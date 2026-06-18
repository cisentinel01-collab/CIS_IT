from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
                             QTableWidgetItem, QPushButton, QLineEdit, QLabel,
                             QHeaderView, QComboBox, QMessageBox)
from PySide6.QtCore import Qt
from models.location import Location

class LocationsView(QWidget):
    def __init__(self):
        super().__init__()
        self.model = Location()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        toolbar = QHBoxLayout()
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("اسم الموقع الجديد (مثلاً: رف A1)")
        toolbar.addWidget(self.name_input)

        add_btn = QPushButton("إضافة موقع")
        add_btn.clicked.connect(self.handle_add)
        toolbar.addWidget(add_btn)
        layout.addLayout(toolbar)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "الاسم", "إجراءات"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)
        self.refresh()

    def refresh(self):
        locs = self.model.get_all()
        self.table.setRowCount(0)
        for l in locs:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(l['id'])))
            self.table.setItem(row, 1, QTableWidgetItem(l['name']))

            del_btn = QPushButton("حذف")
            del_btn.clicked.connect(lambda _, id=l['id']: self.handle_delete(id))
            self.table.setCellWidget(row, 2, del_btn)

    def handle_add(self):
        name = self.name_input.text()
        if name:
            self.model.create({"name": name})
            self.name_input.clear()
            self.refresh()

    def handle_delete(self, id):
        if QMessageBox.question(self, "تأكيد", "هل أنت متأكد؟") == QMessageBox.Yes:
            self.model.soft_delete(id)
            self.refresh()
