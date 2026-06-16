from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
                             QTableWidgetItem, QPushButton, QLineEdit, QHeaderView,
                             QDialog, QFormLayout, QComboBox, QCheckBox, QGroupBox,
                             QMessageBox, QScrollArea)
from PySide6.QtCore import Qt
import qtawesome as qta

class UserManagementView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        toolbar = QHBoxLayout()
        add_btn = QPushButton("إضافة مستخدم جديد")
        add_btn.setObjectName("PrimaryButton")
        add_btn.setIcon(qta.icon("fa5s.user-plus", color="white"))
        add_btn.clicked.connect(self.show_add_dialog)
        toolbar.addWidget(add_btn)
        toolbar.addStretch()
        layout.addLayout(toolbar)

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["اسم المستخدم", "الاسم الكامل", "الدور", "الوظيفة", "القسم", "الحالة", "إجراءات"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        self.refresh()

    def refresh(self):
        users = self.controller.get_all_users()
        self.table.setRowCount(0)
        for u in users:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(u['username']))
            self.table.setItem(row, 1, QTableWidgetItem(u['full_name']))
            self.table.setItem(row, 2, QTableWidgetItem(u['role']))
            self.table.setItem(row, 3, QTableWidgetItem(u['job_title'] or ""))
            self.table.setItem(row, 4, QTableWidgetItem(u['department'] or ""))
            self.table.setItem(row, 5, QTableWidgetItem("نشط" if u['status'] == 'active' else "معطل"))

            edit_btn = QPushButton("تعديل")
            edit_btn.setStyleSheet("background-color: #f39c12; color: white; border-radius: 3px;")
            edit_btn.clicked.connect(lambda _, user=u: self.show_edit_dialog(user))
            self.table.setCellWidget(row, 6, edit_btn)

    def show_add_dialog(self):
        dialog = UserDialog(self)
        if dialog.exec():
            data, perms = dialog.get_data()
            try:
                self.controller.add_user(data, perms)
                self.refresh()
                QMessageBox.information(self, "نجاح", "تمت إضافة المستخدم بنجاح")
            except Exception as e:
                QMessageBox.critical(self, "خطأ", f"فشل إضافة المستخدم: {str(e)}")

    def show_edit_dialog(self, user):
        dialog = UserDialog(self, user)
        perms = self.controller.get_permissions(user['id'])
        dialog.load_data(user, perms)
        if dialog.exec():
            data, permissions = dialog.get_data()
            try:
                self.controller.update_user(user['id'], data, permissions)
                self.refresh()
                QMessageBox.information(self, "نجاح", "تم تحديث بيانات المستخدم بنجاح")
            except Exception as e:
                QMessageBox.critical(self, "خطأ", f"فشل تحديث المستخدم: {str(e)}")

class UserDialog(QDialog):
    def __init__(self, parent=None, user_data=None):
        super().__init__(parent)
        self.user_data = user_data
        self.setWindowTitle("إدارة المستخدم")
        self.resize(600, 700)
        self.setLayoutDirection(Qt.RightToLeft)
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        form_layout = QFormLayout(scroll_content)

        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.full_name_input = QLineEdit()
        self.role_combo = QComboBox()
        self.role_combo.addItems(["admin", "warehouse_keeper", "supervisor"])
        self.job_title_input = QLineEdit()
        self.dept_input = QLineEdit()

        form_layout.addRow("اسم المستخدم:", self.username_input)
        form_layout.addRow("كلمة المرور:", self.password_input)
        form_layout.addRow("الاسم الكامل:", self.full_name_input)
        form_layout.addRow("الدور الوظيفي:", self.role_combo)
        form_layout.addRow("المسمى الوظيفي:", self.job_title_input)
        form_layout.addRow("القسم:", self.dept_input)

        # Permissions Group
        self.perm_checks = {}
        modules = [
            ("items", "الأصناف"),
            ("suppliers", "الموردين"),
            ("stock", "المخزون"),
            ("requests", "طلبات الشراء"),
            ("reports", "التقارير"),
            ("users", "المستخدمين"),
            ("settings", "الإعدادات")
        ]

        perm_group = QGroupBox("الصلاحيات")
        perm_layout = QVBoxLayout(perm_group)

        for mod_key, mod_name in modules:
            mod_row = QHBoxLayout()
            mod_row.addWidget(QLabel(f"<b>{mod_name}</b>"), 1)

            checks = {}
            for action in ["view", "add", "edit", "delete", "print", "export"]:
                cb = QCheckBox(self._translate_action(action))
                mod_row.addWidget(cb)
                checks[f"can_{action}"] = cb

            self.perm_checks[mod_key] = checks
            perm_layout.addLayout(mod_row)

        form_layout.addRow(perm_group)

        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)

        btns = QHBoxLayout()
        save_btn = QPushButton("حفظ")
        save_btn.setObjectName("PrimaryButton")
        save_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("إلغاء")
        cancel_btn.clicked.connect(self.reject)
        btns.addWidget(save_btn)
        btns.addWidget(cancel_btn)
        main_layout.addLayout(btns)

    def _translate_action(self, action):
        trans = {"view": "عرض", "add": "إضافة", "edit": "تعديل", "delete": "حذف", "print": "طباعة", "export": "تصدير"}
        return trans.get(action, action)

    def load_data(self, user, perms):
        self.username_input.setText(user['username'])
        self.username_input.setReadOnly(True)
        self.full_name_input.setText(user['full_name'])
        self.role_combo.setCurrentText(user['role'])
        self.job_title_input.setText(user['job_title'] or "")
        self.dept_input.setText(user['department'] or "")

        for mod, checks in self.perm_checks.items():
            if mod in perms:
                for action, cb in checks.items():
                    cb.setChecked(perms[mod][action] == 1)

    def accept(self):
        from utils.validator import Validator
        if not Validator.is_not_empty(self.username_input.text()) or \
           not Validator.is_not_empty(self.full_name_input.text()):
            QMessageBox.warning(self, "تنبيه", "يرجى ملأ البيانات الأساسية")
            return
        if not self.user_data and not Validator.is_not_empty(self.password_input.text()):
            QMessageBox.warning(self, "تنبيه", "يرجى إدخال كلمة المرور للمستخدم الجديد")
            return
        super().accept()

    def get_data(self):
        user_data = {
            "username": self.username_input.text(),
            "full_name": self.full_name_input.text(),
            "role": self.role_combo.currentText(),
            "job_title": self.job_title_input.text(),
            "department": self.dept_input.text()
        }
        if self.password_input.text():
            user_data["password"] = self.password_input.text()

        permissions = {}
        for mod, checks in self.perm_checks.items():
            permissions[mod] = {k: (1 if cb.isChecked() else 0) for k, cb in checks.items()}

        return user_data, permissions
