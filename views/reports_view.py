from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QFrame, QGridLayout, QMessageBox)
from PySide6.QtCore import Qt
import qtawesome as qta
import os

class ReportsView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)

        grid = QGridLayout()
        grid.setSpacing(20)

        reports = [
            ("تقرير المخزون الحالي", "fa5s.clipboard-list", self.export_inventory),
            ("تقرير الوارد", "fa5s.file-import", lambda: self.export_movements('IN')),
            ("تقرير الصادر", "fa5s.file-export", lambda: self.export_movements('OUT')),
            ("تقرير حسب المورد", "fa5s.truck", self.export_supplier_report),
            ("تقرير الأصناف منخفضة المخزون", "fa5s.exclamation-triangle", self.export_low_stock),
            ("سجل نشاط المستخدمين", "fa5s.user-shield", self.export_user_activity),
        ]

        row, col = 0, 0
        for title, icon, callback in reports:
            btn = self.create_report_button(title, icon, callback)
            grid.addWidget(btn, row, col)
            col += 1
            if col > 1:
                col = 0
                row += 1

        layout.addLayout(grid)
        layout.addStretch()

    def create_report_button(self, title, icon_name, callback):
        btn = QPushButton()
        btn.setFixedSize(300, 150)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                border: 2px solid #1a2a6c;
                border-radius: 15px;
                text-align: center;
                font-size: 16px;
                font-weight: bold;
                color: #1a2a6c;
            }
            QPushButton:hover {
                background-color: #f5f6fa;
                border: 2px solid #d4af37;
            }
        """)

        layout = QVBoxLayout(btn)
        icon_label = QLabel()
        icon_label.setPixmap(qta.icon(icon_name, color="#1a2a6c").pixmap(50, 50))
        icon_label.setAlignment(Qt.AlignCenter)

        text_label = QLabel(title)
        text_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(icon_label)
        layout.addWidget(text_label)

        btn.clicked.connect(callback)
        return btn

    def export_inventory(self):
        try:
            path = self.controller.export_inventory_to_excel()
            QMessageBox.information(self, "نجاح", f"تم تصدير التقرير بنجاح إلى:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "خطأ", str(e))

    def export_movements(self, type=None):
        try:
            path = self.controller.export_movements_to_excel(type=type)
            QMessageBox.information(self, "نجاح", f"تم تصدير التقرير بنجاح إلى:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "خطأ", str(e))

    def export_supplier_report(self):
        from models.supplier import Supplier
        suppliers = Supplier().get_all()
        if not suppliers:
            QMessageBox.warning(self, "تنبيه", "لا يوجد موردين")
            return

        from PySide6.QtWidgets import QInputDialog
        names = [s['name'] for s in suppliers]
        name, ok = QInputDialog.getItem(self, "اختيار المورد", "اختر المورد للتقرير:", names, 0, False)
        if ok and name:
            s_id = next(s['id'] for s in suppliers if s['name'] == name)
            try:
                path = self.controller.export_supplier_report(s_id)
                QMessageBox.information(self, "نجاح", f"تم تصدير التقرير بنجاح إلى:\n{path}")
            except Exception as e:
                QMessageBox.critical(self, "خطأ", str(e))

    def export_low_stock(self):
        try:
            from models.item import Item
            items = Item().get_low_stock()
            headers = ["كود الصنف", "اسم الصنف", "الكمية الحالية", "الحد الأدنى"]
            data = [[i['code'], i['name'], i['current_stock'], i['min_stock']] for i in items]

            from utils.excel_gen import ExcelGenerator
            import datetime
            filename = f"reports/low_stock_{datetime.datetime.now().strftime('%Y%m%d')}.xlsx"
            ExcelGenerator().export_data(filename, headers, data, "Low Stock Report")
            QMessageBox.information(self, "نجاح", f"تم تصدير التقرير بنجاح إلى:\n{filename}")
        except Exception as e:
            QMessageBox.critical(self, "خطأ", str(e))

    def export_user_activity(self):
        try:
            logs = self.controller.get_user_activity()
            headers = ["الوقت", "المستخدم", "العملية", "التفاصيل"]
            data = [[l['timestamp'], l['username'], l['action'], l['details'] or ""] for l in logs]

            from utils.excel_gen import ExcelGenerator
            import datetime
            filename = f"reports/user_activity_{datetime.datetime.now().strftime('%Y%m%d')}.xlsx"
            ExcelGenerator().export_data(filename, headers, data, "User Activity Report")
            QMessageBox.information(self, "نجاح", f"تم تصدير التقرير بنجاح إلى:\n{filename}")
        except Exception as e:
            QMessageBox.critical(self, "خطأ", str(e))
