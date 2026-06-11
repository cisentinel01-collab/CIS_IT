from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
                             QTableWidgetItem, QPushButton, QLineEdit, QHeaderView,
                             QDialog, QFormLayout, QMessageBox)
from PySide6.QtCore import Qt
import qtawesome as qta

class LocationsView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        toolbar = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("بحث عن موقع...")
        toolbar.addWidget(self.search_input)

        add_btn = QPushButton("إضافة موقع")
        add_btn.setObjectName("PrimaryButton")
        add_btn.setIcon(qta.icon("fa5s.plus", color="white"))
        add_btn.clicked.connect(self.show_add_dialog)
        toolbar.addWidget(add_btn)

        layout.addLayout(toolbar)

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["اسم الموقع", "الوصف"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        self.refresh()

    def refresh(self):
        locations = self.controller.get_all()
        self.table.setRowCount(0)
        for loc in locations:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(loc['name']))
            self.table.setItem(row, 1, QTableWidgetItem(loc['description'] or ""))

    def show_add_dialog(self):
        dialog = LocationDialog(self)
        if dialog.exec():
            data = dialog.get_data()
            self.controller.create(data)
            self.refresh()

class LocationDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("إضافة موقع جديد")
        self.setLayoutDirection(Qt.RightToLeft)
        self.setup_ui()

    def setup_ui(self):
        layout = QFormLayout(self)
        self.name_input = QLineEdit()
        self.desc_input = QLineEdit()
        layout.addRow("اسم الموقع:", self.name_input)
        layout.addRow("الوصف:", self.desc_input)

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
            "description": self.desc_input.text()
        }
