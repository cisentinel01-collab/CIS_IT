from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
                             QTableWidgetItem, QPushButton, QLineEdit, QHeaderView,
                             QDialog, QFormLayout, QMessageBox)
from PySide6.QtCore import Qt
import qtawesome as qta

class SuppliersView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        toolbar = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("بحث عن مورد...")
        self.search_input.textChanged.connect(self.handle_search)
        toolbar.addWidget(self.search_input)

        add_btn = QPushButton("إضافة مورد")
        add_btn.setObjectName("PrimaryButton")
        add_btn.setIcon(qta.icon("fa5s.plus", color="white"))
        add_btn.clicked.connect(self.show_add_dialog)
        toolbar.addWidget(add_btn)

        layout.addLayout(toolbar)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["الاسم", "الهاتف", "البريد الإلكتروني", "العنوان"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        self.refresh()

    def refresh(self, suppliers=None):
        if suppliers is None:
            suppliers = self.controller.get_all_suppliers()

        self.table.setRowCount(0)
        for s in suppliers:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(s['name']))
            self.table.setItem(row, 1, QTableWidgetItem(s['phone'] or ""))
            self.table.setItem(row, 2, QTableWidgetItem(s['email'] or ""))
            self.table.setItem(row, 3, QTableWidgetItem(s['address'] or ""))

    def handle_search(self):
        term = self.search_input.text()
        if term:
            suppliers = self.controller.search_suppliers(term)
            self.refresh(suppliers)
        else:
            self.refresh()

    def show_add_dialog(self):
        dialog = SupplierDialog(self)
        if dialog.exec():
            data = dialog.get_data()
            self.controller.add_supplier(data)
            self.refresh()

class SupplierDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("إضافة مورد جديد")
        self.setLayoutDirection(Qt.RightToLeft)
        self.setup_ui()

    def setup_ui(self):
        layout = QFormLayout(self)

        self.name_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.email_input = QLineEdit()
        self.address_input = QLineEdit()

        layout.addRow("اسم المورد:", self.name_input)
        layout.addRow("رقم الهاتف:", self.phone_input)
        layout.addRow("البريد الإلكتروني:", self.email_input)
        layout.addRow("العنوان:", self.address_input)

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
            "name": self.name_input.text(),
            "phone": self.phone_input.text(),
            "email": self.email_input.text(),
            "address": self.address_input.text()
        }
