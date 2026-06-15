from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
                             QTableWidgetItem, QPushButton, QLineEdit, QLabel,
                             QHeaderView, QDialog, QFormLayout, QComboBox,
                             QSpinBox, QMessageBox, QFileDialog)
from PySide6.QtCore import Qt
import qtawesome as qta
import os

class ItemsView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        # Toolbar
        toolbar = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("بحث عن صنف...")
        self.search_input.textChanged.connect(self.handle_search)
        toolbar.addWidget(self.search_input)

        add_btn = QPushButton("إضافة صنف")
        add_btn.setObjectName("PrimaryButton")
        add_btn.setIcon(qta.icon("fa5s.plus", color="white"))
        add_btn.clicked.connect(self.show_add_dialog)
        toolbar.addWidget(add_btn)

        scan_btn = QPushButton("قراءة QR")
        scan_btn.setObjectName("GoldButton")
        scan_btn.setIcon(qta.icon("fa5s.qrcode", color="white"))
        scan_btn.clicked.connect(self.handle_scan)
        toolbar.addWidget(scan_btn)

        import_btn = QPushButton("استيراد")
        import_btn.setObjectName("SecondaryButton")
        import_btn.clicked.connect(self.handle_import)
        toolbar.addWidget(import_btn)

        layout.addLayout(toolbar)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["الكود", "الاسم", "الفئة", "الوحدة", "الموقع", "الكمية", "الحد الأدنى"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        self.refresh()

    def refresh(self, items=None):
        if items is None:
            items = self.controller.get_all_items()

        self.table.setRowCount(0)
        for item in items:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(item['code'])))
            self.table.setItem(row, 1, QTableWidgetItem(str(item['name'])))
            self.table.setItem(row, 2, QTableWidgetItem(str(item['category'] or "")))
            self.table.setItem(row, 3, QTableWidgetItem(str(item['unit'] or "")))
            self.table.setItem(row, 4, QTableWidgetItem(str(item['location_name'] or "")))
            self.table.setItem(row, 5, QTableWidgetItem(str(item['current_stock'])))
            self.table.setItem(row, 6, QTableWidgetItem(str(item['min_stock'])))

    def handle_search(self):
        term = self.search_input.text()
        if term:
            items = self.controller.search_items(term)
            self.refresh(items)
        else:
            self.refresh()

    def handle_scan(self):
        # Mocking QR scan
        code, ok = QMessageBox.getText(self, "مسح QR", "يرجى مسح كود QR أو إدخال الكود يدوياً:")
        if ok and code:
            from models.item import Item
            item = Item().get_by_code(code)
            if item:
                self.search_input.setText(code)
            else:
                QMessageBox.warning(self, "تنبيه", "الصنف غير موجود")

    def show_add_dialog(self):
        dialog = ItemDialog(self)
        if dialog.exec():
            data = dialog.get_data()
            self.controller.add_item(data)
            self.refresh()

    def handle_import(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "اختر ملف Excel", "", "Excel Files (*.xlsx *.xls)")
        if file_path:
            try:
                from utils.excel_gen import ExcelGenerator
                items = ExcelGenerator().import_items(file_path)
                for item in items:
                    self.controller.add_item(item)
                self.refresh()
                QMessageBox.information(self, "نجاح", f"تم استيراد {len(items)} صنف بنجاح")
            except Exception as e:
                QMessageBox.critical(self, "خطأ", f"فشل الاستيراد: {str(e)}")

class ItemDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("إضافة صنف جديد")
        self.setLayoutDirection(Qt.RightToLeft)
        self.setup_ui()

    def setup_ui(self):
        layout = QFormLayout(self)

        self.code_input = QLineEdit()
        self.name_input = QLineEdit()
        self.category_input = QLineEdit()
        self.unit_input = QLineEdit()
        self.min_stock_input = QSpinBox()
        self.min_stock_input.setMaximum(1000000)

        layout.addRow("كود الصنف:", self.code_input)
        layout.addRow("اسم الصنف:", self.name_input)
        layout.addRow("الفئة:", self.category_input)
        layout.addRow("الوحدة:", self.unit_input)
        layout.addRow("الحد الأدنى:", self.min_stock_input)

        btns = QHBoxLayout()
        save_btn = QPushButton("حفظ")
        save_btn.setObjectName("PrimaryButton")
        save_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("إلغاء")
        cancel_btn.clicked.connect(self.reject)
        btns.addWidget(save_btn)
        btns.addWidget(cancel_btn)
        layout.addRow(btns)

    def get_data(self):
        return {
            "code": self.code_input.text(),
            "name": self.name_input.text(),
            "category": self.category_input.text(),
            "unit": self.unit_input.text(),
            "min_stock": self.min_stock_input.value()
        }
