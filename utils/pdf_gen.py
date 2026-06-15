import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from arabic_reshaper import reshape
from bidi.algorithm import get_display

# Note: We might need to install arabic-reshaper and python-bidi
# Let's check if they are available or install them.

class PDFGenerator:
    def __init__(self):
        self.font_path = "assets/fonts/Cairo-Regular.ttf"
        self.bold_font_path = "assets/fonts/Cairo-Bold.ttf"
        try:
            if os.path.exists(self.font_path):
                pdfmetrics.registerFont(TTFont('Cairo', self.font_path))
                pdfmetrics.registerFont(TTFont('Cairo-Bold', self.bold_font_path))
                self.font_name = 'Cairo'
            else:
                self.font_name = 'Helvetica'
        except Exception as e:
            print(f"Font registration error: {e}")
            self.font_name = 'Helvetica'

    def _prepare_arabic(self, text):
        if not text:
            return ""
        try:
            from arabic_reshaper import reshape
            from bidi.algorithm import get_display
            reshaped_text = reshape(text)
            bidi_text = get_display(reshaped_text)
            return bidi_text
        except ImportError:
            return text

    def generate_invoice(self, filename, data, items, company_info):
        doc = SimpleDocTemplate(filename, pagesize=A4)
        elements = []

        styles = getSampleStyleSheet()
        arabic_style = ParagraphStyle(
            'ArabicStyle',
            parent=styles['Normal'],
            fontName=self.font_name,
            alignment=2, # Right alignment
            fontSize=12
        )

        # Header
        logo_path = "logo/logo.png"
        if not os.path.exists(logo_path) and company_info and company_info['logo_path']:
            logo_path = company_info['logo_path']

        if os.path.exists(logo_path):
            try:
                elements.append(Image(logo_path, width=100, height=100))
                elements.append(Spacer(1, 12))
            except:
                pass

        company_name = company_info['company_name'] if company_info else 'American Marine Services'
        elements.append(Paragraph(self._prepare_arabic(company_name), arabic_style))
        elements.append(Spacer(1, 12))

        title_text = data.get('report_title')
        if not title_text:
            title_text = "فاتورة وارد" if data['type'] == 'IN' else "سند صرف"

        elements.append(Paragraph(self._prepare_arabic(title_text), arabic_style))
        elements.append(Spacer(1, 20))

        # Info Table
        info_data = [
            [self._prepare_arabic(f"التاريخ: {data['date']}"), self._prepare_arabic(f"الرقم: {data['reference_no']}")],
        ]
        if data['type'] == 'IN':
            supplier_name = data['supplier_name'] if 'supplier_name' in data.keys() else ""
            info_data.append([self._prepare_arabic(f"المورد: {supplier_name}"), ""])
        else:
            receiver_name = data['receiver_name'] if 'receiver_name' in data.keys() else ""
            info_data.append([self._prepare_arabic(f"المستلم: {receiver_name}"), ""])

        info_table = Table(info_data, colWidths=[250, 250])
        elements.append(info_table)
        elements.append(Spacer(1, 20))

        # Items Table
        table_data = [[self._prepare_arabic("الإجمالي"), self._prepare_arabic("السعر"), self._prepare_arabic("الكمية"), self._prepare_arabic("الصنف")]]
        for item in items:
            price = item['price'] if 'price' in item.keys() else 0
            total = item['quantity'] * price
            table_data.append([
                f"{total:,.2f}",
                f"{price:,.2f}",
                str(item['quantity']),
                self._prepare_arabic(item['item_name'])
            ])

        item_table = Table(table_data, colWidths=[100, 100, 100, 200])
        font_bold = f"{self.font_name}-Bold" if self.font_name == 'Cairo' else 'Helvetica-Bold'
        item_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), self.font_name),
            ('FONTNAME', (0, 0), (-1, 0), font_bold),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(item_table)
        elements.append(Spacer(1, 20))

        # Totals and Discounts
        if 'subtotal' in data.keys():
            totals_data = [
                [f"{data['subtotal']:,.2f}", self._prepare_arabic("المجموع الفرعي:")],
                [f"{data['discount_amount']:,.2f} ({data['discount_percent']}%)", self._prepare_arabic("الخصم:")],
                [f"{data['final_total']:,.2f}", self._prepare_arabic("الإجمالي النهائي:")]
            ]
            totals_table = Table(totals_data, colWidths=[100, 100])
            totals_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
                ('FONTNAME', (0, 0), (-1, -1), self.font_name),
                ('FONTNAME', (0, 2), (-1, 2), f"{self.font_name}-Bold"),
            ]))
            elements.append(totals_table)

        doc.build(elements)
