from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit,
                             QPushButton, QLabel, QGroupBox, QMessageBox, QFileDialog)
from PySide6.QtCore import Qt
from models.settings import Settings
from utils.backup_manager import BackupManager

class SettingsView(QWidget):
    def __init__(self):
        super().__init__()
        self.settings_model = Settings()
        self.backup_mgr = BackupManager()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        # Company Info
        company_group = QGroupBox("بيانات الشركة")
        company_layout = QFormLayout(company_group)

        settings = self.settings_model.get_settings()

        self.name_input = QLineEdit(settings['company_name'] if settings else "")
        self.address_input = QLineEdit(settings['address'] if settings else "")
        self.phone_input = QLineEdit(settings['phone'] if settings else "")
        self.email_input = QLineEdit(settings['email'] if settings else "")
        self.logo_path_input = QLineEdit(settings['logo_path'] if settings else "")

        company_layout.addRow("اسم الشركة:", self.name_input)
        company_layout.addRow("العنوان:", self.address_input)
        company_layout.addRow("رقم الهاتف:", self.phone_input)
        company_layout.addRow("البريد الإلكتروني:", self.email_input)

        logo_row = QHBoxLayout()
        logo_row.addWidget(self.logo_path_input)
        browse_btn = QPushButton("تصفح")
        browse_btn.clicked.connect(self.browse_logo)
        logo_row.addWidget(browse_btn)
        company_layout.addRow("مسار الشعار:", logo_row)

        save_btn = QPushButton("حفظ التغييرات")
        save_btn.setObjectName("PrimaryButton")
        save_btn.clicked.connect(self.save_settings)
        company_layout.addRow(save_btn)

        layout.addWidget(company_group)

        # Backup & Restore
        backup_group = QGroupBox("النسخ الاحتياطي")
        backup_layout = QVBoxLayout(backup_group)

        create_backup_btn = QPushButton("إنشاء نسخة احتياطية الآن")
        create_backup_btn.setObjectName("GoldButton")
        create_backup_btn.clicked.connect(self.handle_backup)
        backup_layout.addWidget(create_backup_btn)

        layout.addWidget(backup_group)
        layout.addStretch()

    def browse_logo(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "اختر الشعار", "", "Image Files (*.png *.jpg *.jpeg)")
        if file_path:
            self.logo_path_input.setText(file_path)

    def save_settings(self):
        data = {
            "company_name": self.name_input.text(),
            "address": self.address_input.text(),
            "phone": self.phone_input.text(),
            "email": self.email_input.text(),
            "logo_path": self.logo_path_input.text()
        }
        self.settings_model.update_settings(data)
        QMessageBox.information(self, "نجاح", "تم حفظ الإعدادات بنجاح")

    def handle_backup(self):
        path = self.backup_mgr.create_backup()
        if path:
            QMessageBox.information(self, "نجاح", f"تم إنشاء النسخة الاحتياطية بنجاح في:\n{path}")
        else:
            QMessageBox.critical(self, "خطأ", "فشل إنشاء النسخة الاحتياطية")
