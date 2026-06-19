from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
                             QTableWidgetItem, QPushButton, QLineEdit, QLabel,
                             QHeaderView, QGroupBox, QDialog, QFormLayout, QComboBox, QMessageBox)
from PySide6.QtCore import Qt
import qtawesome as qta

class UserManagementView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        toolbar = QHBoxLayout()
        add_btn = QPushButton("إضافة مستخدم")
        add_btn.setObjectName("PrimaryButton")
        add_btn.clicked.connect(self.show_add_dialog)
        toolbar.addWidget(add_btn)
        layout.addLayout(toolbar)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "الاسم الكامل", "اسم المستخدم", "الدور"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)
        self.refresh()

    def refresh(self):
        users = self.controller.get_all_users()
        self.table.setRowCount(0)
        for u in users:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(u['id'])))
            self.table.setItem(row, 1, QTableWidgetItem(u['full_name']))
            self.table.setItem(row, 2, QTableWidgetItem(u['username']))

            role_map = {"warehouse_manager": "مسؤول مخزن", "follow_up": "المتابعة"}
            self.table.setItem(row, 3, QTableWidgetItem(role_map.get(u['role'], u['role'])))

            del_btn = QPushButton()
            del_btn.setIcon(qta.icon("fa5s.trash-alt", color="white"))
            del_btn.setFixedSize(30, 30)
            del_btn.setStyleSheet("background-color: #e74c3c; border-radius: 5px;")
            del_btn.clicked.connect(lambda _, user=u: self.handle_delete(user))
            self.table.setCellWidget(row, 4, del_btn)

    def handle_delete(self, user):
        if QMessageBox.question(self, "تأكيد", f"حذف المستخدم '{user['username']}'؟") == QMessageBox.Yes:
            self.controller.model.update(user['id'], {"is_active": 0})
            self.refresh()

    def show_add_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("إضافة مستخدم")
        d_layout = QFormLayout(dialog)

        full_name = QLineEdit()
        username = QLineEdit()
        password = QLineEdit()
        role = QComboBox()
        role.addItem("مسؤول مخزن", "warehouse_manager")
        role.addItem("المتابعة", "follow_up")

        d_layout.addRow("الاسم الكامل:", full_name)
        d_layout.addRow("اسم المستخدم:", username)
        d_layout.addRow("كلمة المرور:", password)
        d_layout.addRow("الدور:", role)

        save = QPushButton("حفظ")
        save.clicked.connect(lambda: self.save_user(dialog, {
            "full_name": full_name.text(),
            "username": username.text(),
            "password": password.text(),
            "role": role.currentData()
        }))
        d_layout.addRow(save)
        dialog.exec()

    def save_user(self, dialog, data):
        self.controller.add_user(data)
        dialog.accept()
        self.refresh()
