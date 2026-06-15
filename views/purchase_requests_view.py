from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
                             QTableWidgetItem, QPushButton, QLineEdit, QHeaderView,
                             QDialog, QFormLayout, QComboBox, QSpinBox, QMessageBox,
                             QLabel, QGroupBox)
from PySide6.QtCore import Qt
import qtawesome as qta
from models.item import Item
from utils.auth import AuthManager

class PurchaseRequestsView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        toolbar = QHBoxLayout()
        add_btn = QPushButton("إنشاء طلب شراء")
        add_btn.setObjectName("PrimaryButton")
        add_btn.setIcon(qta.icon("fa5s.plus", color="white"))
        add_btn.clicked.connect(self.show_add_dialog)
        toolbar.addWidget(add_btn)

        refresh_btn = QPushButton("تحديث")
        refresh_btn.clicked.connect(self.refresh)
        toolbar.addWidget(refresh_btn)

        toolbar.addStretch()
        layout.addLayout(toolbar)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["رقم الطلب", "القسم", "مقدم الطلب", "الحالة", "التاريخ", "إجراءات"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        self.refresh()

    def refresh(self):
        requests = self.controller.get_all_requests()
        self.table.setRowCount(0)
        for req in requests:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(req['request_no']))
            self.table.setItem(row, 1, QTableWidgetItem(req['department']))
            self.table.setItem(row, 2, QTableWidgetItem(req['requester_name']))
            self.table.setItem(row, 3, QTableWidgetItem(self._translate_status(req['status'])))
            self.table.setItem(row, 4, QTableWidgetItem(req['date']))

            actions_layout = QHBoxLayout()
            actions_layout.setContentsMargins(0, 0, 0, 0)

            view_btn = QPushButton("عرض")
            view_btn.clicked.connect(lambda _, r=req: self.view_request(r))
            actions_layout.addWidget(view_btn)

            if req['status'] == 'pending' and AuthManager.has_permission('requests', 'can_edit'):
                approve_btn = QPushButton("اعتماد")
                approve_btn.setStyleSheet("background-color: #2ecc71; color: white;")
                approve_btn.clicked.connect(lambda _, r=req: self.handle_approval(r['id'], "approved"))
                actions_layout.addWidget(approve_btn)

                reject_btn = QPushButton("رفض")
                reject_btn.setStyleSheet("background-color: #e74c3c; color: white;")
                reject_btn.clicked.connect(lambda _, r=req: self.handle_approval(r['id'], "rejected"))
                actions_layout.addWidget(reject_btn)

            cell_widget = QWidget()
            cell_widget.setLayout(actions_layout)
            self.table.setCellWidget(row, 5, cell_widget)

    def _translate_status(self, status):
        trans = {"pending": "قيد الانتظار", "approved": "تم الاعتماد", "rejected": "مرفوض"}
        return trans.get(status, status)

    def show_add_dialog(self):
        dialog = RequestDialog(self)
        if dialog.exec():
            data, items = dialog.get_data()
            self.controller.create_request(data, items)
            self.refresh()

    def view_request(self, req):
        details = self.controller.get_details(req['id'])
        msg = f"تفاصيل الطلب: {req['request_no']}\n\n"
        for d in details:
            msg += f"- {d['item_name']}: {d['quantity']} {d['unit']}\n"
        QMessageBox.information(self, "تفاصيل الطلب", msg)

    def handle_approval(self, request_id, status):
        if status == "approved":
            self.controller.approve_request(request_id)
        else:
            reason, ok = QMessageBox.getText(self, "سبب الرفض", "يرجى إدخال سبب الرفض:")
            if ok:
                self.controller.reject_request(request_id, reason)
        self.refresh()

class RequestDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("إنشاء طلب شراء")
        self.resize(500, 600)
        self.setLayoutDirection(Qt.RightToLeft)
        self.items_to_request = []
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        info_group = QGroupBox("بيانات الطلب")
        form = QFormLayout(info_group)
        self.dept_input = QLineEdit()
        self.requester_input = QLineEdit()
        form.addRow("القسم الطالب:", self.dept_input)
        form.addRow("اسم مقدم الطلب:", self.requester_input)
        layout.addWidget(info_group)

        item_group = QGroupBox("إضافة أصناف")
        item_layout = QHBoxLayout(item_group)
        self.item_combo = QComboBox()
        for i in Item().get_all():
            self.item_combo.addItem(i['name'], i['id'])
        self.qty_input = QSpinBox()
        self.qty_input.setMaximum(1000000)
        add_btn = QPushButton("إضافة")
        add_btn.clicked.connect(self.add_item)
        item_layout.addWidget(self.item_combo, 2)
        item_layout.addWidget(self.qty_input)
        item_layout.addWidget(add_btn)
        layout.addWidget(item_group)

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["الصنف", "الكمية"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        btns = QHBoxLayout()
        save_btn = QPushButton("إرسال الطلب")
        save_btn.setObjectName("PrimaryButton")
        save_btn.clicked.connect(self.accept)
        btns.addWidget(save_btn)
        layout.addLayout(btns)

    def add_item(self):
        item_id = self.item_combo.currentData()
        item_name = self.item_combo.currentText()
        qty = self.qty_input.value()
        if qty <= 0: return

        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(item_name))
        self.table.setItem(row, 1, QTableWidgetItem(str(qty)))
        self.items_to_request.append({"item_id": item_id, "quantity": qty})

    def get_data(self):
        data = {
            "department": self.dept_input.text(),
            "requester_name": self.requester_input.text()
        }
        return data, self.items_to_request
