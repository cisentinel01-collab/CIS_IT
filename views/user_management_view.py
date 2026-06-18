from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
                             QTableWidgetItem, QPushButton, QLineEdit, QLabel,
                             QHeaderView, QGroupBox)
from PySide6.QtCore import Qt

class UserManagementView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

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
            self.table.setItem(row, 3, QTableWidgetItem(u['role']))
