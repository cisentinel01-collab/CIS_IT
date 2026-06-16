from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
                             QTableWidgetItem, QPushButton, QLineEdit, QHeaderView,
                             QDialog, QFormLayout, QMessageBox)
from PySide6.QtCore import Qt
import qtawesome as qta

from PySide6.QtCore import Qt, Signal

class SuppliersView(QWidget):
    data_changed = Signal()

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
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["الاسم", "الهاتف", "البريد الإلكتروني", "العنوان"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        self.refresh()

    def refresh(self, suppliers=None):
        if suppliers is None:
            suppliers = self.controller.get_all_suppliers()

        self.table.setRowCount(0)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["الاسم", "الهاتف", "البريد الإلكتروني", "العنوان", "إجراءات"])

        for s in suppliers:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(s['name']))
            self.table.setItem(row, 1, QTableWidgetItem(s['phone'] or ""))
            self.table.setItem(row, 2, QTableWidgetItem(s['email'] or ""))
            self.table.setItem(row, 3, QTableWidgetItem(s['address'] or ""))

            edit_btn = QPushButton("تعديل")
            edit_btn.setStyleSheet("background-color: #f39c12; color: white; border-radius: 3px;")
            edit_btn.clicked.connect(lambda _, sup=s: self.show_edit_dialog(sup))
            self.table.setCellWidget(row, 4, edit_btn)

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
            self.data_changed.emit()

    def show_edit_dialog(self, supplier):
        from utils.auth import AuthManager
        if not AuthManager.has_permission('suppliers', 'can_edit'):
            QMessageBox.warning(self, "تنبيه", "لا تملك صلاحية التعديل")
            return

        dialog = SupplierDialog(self, supplier)
        if dialog.exec():
            data = dialog.get_data()
            self.controller.update_supplier(supplier['id'], data)
            self.refresh()
            self.data_changed.emit()

class SupplierDialog(QDialog):
    def __init__(self, parent=None, supplier_data=None):
        super().__init__(parent)
        self.supplier_data = supplier_data
        self.setWindowTitle("تعديل مورد" if supplier_data else "إضافة مورد جديد")
        self.setLayoutDirection(Qt.RightToLeft)
        self.setup_ui()
        if supplier_data:
            self.load_data()

    def load_data(self):
        self.name_input.setText(self.supplier_data['name'])
        self.phone_input.setText(self.supplier_data['phone'] or "")
        self.email_input.setText(self.supplier_data['email'] or "")
        self.address_input.setText(self.supplier_data['address'] or "")

    def setup_ui(self):
        layout = QFormLayout(self)
        from utils.validator import Validator

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("أدخل اسم الشركة الموردة")
        Validator.setup_strict_validation(self.name_input, "name")

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("أرقام فقط")
        Validator.setup_strict_validation(self.phone_input, "phone")

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("example@domain.com")

        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText("العنوان التفصيلي")

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

    def accept(self):
        from utils.validator import Validator
        if not Validator.is_not_empty(self.name_input.text()):
            QMessageBox.warning(self, "تنبيه", "يرجى إدخال اسم المورد")
            return
        super().accept()

    def get_data(self):
        return {
            "name": self.name_input.text(),
            "phone": self.phone_input.text(),
            "email": self.email_input.text(),
            "address": self.address_input.text()
        }
