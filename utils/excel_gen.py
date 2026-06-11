import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill

class ExcelGenerator:
    def export_data(self, filename, headers, data, title="Report"):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = title
        ws.sheet_view.rightToLeft = True

        # Style for headers
        header_fill = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
        header_font = Font(color="FFFFFF", bold=True)

        # Add headers
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col, value=header)
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal="center")

        # Add data
        for row_idx, row_data in enumerate(data, 2):
            for col_idx, value in enumerate(row_data, 1):
                cell = ws.cell(row=row_idx, column=col_idx, value=value)
                cell.alignment = Alignment(horizontal="center")

        wb.save(filename)

    def import_items(self, filename):
        wb = openpyxl.load_workbook(filename)
        ws = wb.active
        items = []
        # Assume headers are: Code, Name, Category, Unit, Min Stock
        for row in ws.iter_rows(min_row=2, values_only=True):
            if any(row):
                items.append({
                    "code": row[0],
                    "name": row[1],
                    "category": row[2],
                    "unit": row[3],
                    "min_stock": row[4]
                })
        return items
