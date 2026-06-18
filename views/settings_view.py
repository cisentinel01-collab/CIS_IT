from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
                             QTableWidgetItem, QPushButton, QLineEdit, QLabel,
                             QHeaderView, QGroupBox, QFormLayout, QMessageBox)
from PySide6.QtCore import Qt

class SettingsView(QWidget):
    def __init__(self):
        super().__init__()
        from models.settings import Settings
        self.model = Settings()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        group = QGroupBox("بيانات الشركة")
        form = QFormLayout(group)

        settings = self.model.get_settings() or {}

        self.name = QLineEdit(settings.get('company_name', ''))
        self.address = QLineEdit(settings.get('address', ''))
        self.phone = QLineEdit(settings.get('phone', ''))
        self.email = QLineEdit(settings.get('email', ''))

        form.addRow("اسم الشركة:", self.name)
        form.addRow("العنوان:", self.address)
        form.addRow("الهاتف:", self.phone)
        form.addRow("البريد:", self.email)

        save_btn = QPushButton("حفظ الإعدادات")
        save_btn.setObjectName("PrimaryButton")
        save_btn.clicked.connect(self.handle_save)
        form.addRow(save_btn)

        layout.addWidget(group)
        layout.addStretch()

    def handle_save(self):
        data = {
            "company_name": self.name.text(),
            "address": self.address.text(),
            "phone": self.phone.text(),
            "email": self.email.text()
        }
        self.model.update_settings(data)
        QMessageBox.information(self, "نجاح", "تم حفظ الإعدادات بنجاح")
