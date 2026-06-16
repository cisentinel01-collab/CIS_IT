from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
                             QTableWidgetItem, QPushButton, QLineEdit, QLabel,
                             QHeaderView, QComboBox, QSpinBox, QFormLayout,
                             QGroupBox, QMessageBox)
from PySide6.QtCore import Qt
from models.item import Item
from models.supplier import Supplier

class StockOperationsView(QWidget):
    def __init__(self, controller, op_type="IN"):
        super().__init__()
        self.controller = controller
        self.op_type = op_type # "IN" or "OUT"
        self.items_to_move = []
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        # Header Info
        info_group = QGroupBox("بيانات العملية")
        info_layout = QFormLayout(info_group)

        self.ref_input = QLineEdit()
        self.ref_input.setReadOnly(True)
        self.ref_input.setPlaceholderText("سيتم التوليد تلقائياً")
        self.ref_input.setText(self.controller.generate_invoice_no(self.op_type))
        info_layout.addRow("رقم الفاتورة/العملية:", self.ref_input)

        if self.op_type == "IN":
            self.supplier_combo = QComboBox()
            self.supplier_combo.setToolTip("اختر المورد الذي تم استلام الأصناف منه")
            self.load_suppliers()
            info_layout.addRow("المورد:", self.supplier_combo)

            self.receiver_input = QLineEdit()
            self.receiver_input.setPlaceholderText("أدخل اسم الموظف المستلم")
            from utils.validator import Validator
            Validator.setup_strict_validation(self.receiver_input, "name")
            info_layout.addRow("اسم المستلم:", self.receiver_input)
        else:
            self.issuing_entity = QLineEdit()
            self.issuing_entity.setPlaceholderText("مثال: قسم الصيانة، العميل...")
            from utils.validator import Validator
            Validator.setup_strict_validation(self.issuing_entity, "name")
            info_layout.addRow("الجهة المستلمة:", self.issuing_entity)

            self.receiver_name = QLineEdit()
            self.receiver_name.setPlaceholderText("اسم الشخص الذي تسلم العهدة")
            Validator.setup_strict_validation(self.receiver_name, "name")
            info_layout.addRow("اسم الشخص المستلم:", self.receiver_name)

            self.reason_input = QLineEdit()
            self.reason_input.setPlaceholderText("سبب خروج الأصناف من المخزن")
            info_layout.addRow("سبب الصرف:", self.reason_input)

        layout.addWidget(info_group)

        # Item Selector
        selector_group = QGroupBox("إضافة أصناف")
        selector_layout = QHBoxLayout(selector_group)

        self.item_combo = QComboBox()
        self.load_items()
        selector_layout.addWidget(QLabel("الصنف:"))
        selector_layout.addWidget(self.item_combo, 2)

        self.qty_input = QSpinBox()
        self.qty_input.setMinimum(1)
        self.qty_input.setMaximum(1000000)
        selector_layout.addWidget(QLabel("الكمية:"))
        selector_layout.addWidget(self.qty_input)

        if self.op_type == "IN":
            self.price_input = QLineEdit()
            self.price_input.setPlaceholderText("السعر")
            selector_layout.addWidget(QLabel("السعر:"))
            selector_layout.addWidget(self.price_input)

        add_item_btn = QPushButton("إضافة للقائمة")
        add_item_btn.setObjectName("GoldButton")
        add_item_btn.clicked.connect(self.add_item_to_list)
        selector_layout.addWidget(add_item_btn)

        layout.addWidget(selector_group)

        # Financials
        fin_group = QGroupBox("الإجماليات والخصومات")
        fin_layout = QFormLayout(fin_group)
        self.discount_input = QSpinBox()
        self.discount_input.setSuffix("%")
        self.discount_input.valueChanged.connect(self.update_summary)
        fin_layout.addRow("نسبة الخصم:", self.discount_input)

        self.summary_label = QLabel("المجموع: 0.00 | الخصم: 0.00 | الإجمالي: 0.00")
        self.summary_label.setStyleSheet("font-weight: bold; font-size: 16px; color: #1a2a6c;")
        fin_layout.addRow(self.summary_label)
        layout.addWidget(fin_group)

        # Selected Items Table
        self.table = QTableWidget()
        self.table.setColumnCount(4 if self.op_type == "IN" else 3)
        headers = ["الكود", "الاسم", "الكمية"]
        if self.op_type == "IN": headers.append("السعر")
        self.table.setHorizontalHeaderLabels(headers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        # Submit Button
        submit_btn = QPushButton("إتمام العملية وحفظ PDF")
        submit_btn.setObjectName("PrimaryButton")
        submit_btn.setFixedHeight(50)
        submit_btn.clicked.connect(self.handle_submit)
        layout.addWidget(submit_btn)

    def load_suppliers(self):
        self.supplier_combo.clear()
        suppliers = Supplier().get_all()
        for s in suppliers:
            self.supplier_combo.addItem(s['name'], s['id'])

    def update_summary(self):
        subtotal = sum(item['quantity'] * item.get('price', 0) for item in self.items_to_move)
        discount_pct = self.discount_input.value()
        discount_amt = (subtotal * discount_pct) / 100
        final = subtotal - discount_amt
        self.summary_label.setText(f"المجموع: {subtotal:,.2f} | الخصم: {discount_amt:,.2f} | الإجمالي: {final:,.2f}")

    def load_items(self):
        self.item_combo.clear()
        items = Item().get_all()
        for i in items:
            self.item_combo.addItem(f"{i['code']} - {i['name']}", i)

    def add_item_to_list(self):
        item_data = self.item_combo.currentData()
        if not item_data:
            QMessageBox.warning(self, "تنبيه", "يرجى اختيار صنف أولاً")
            return
        qty = self.qty_input.value()
        if qty <= 0: return

        if self.op_type == "OUT":
            if qty > item_data['current_stock']:
                QMessageBox.warning(self, "تنبيه المخزون",
                                  f"الكمية المطلوبة ({qty}) أكبر من المخزون المتاح ({item_data['current_stock']})")
                return

        price = 0
        if self.op_type == "IN":
            try:
                price_text = self.price_input.text()
                if not price_text:
                    QMessageBox.warning(self, "تنبيه", "يرجى إدخال السعر")
                    return
                price = float(price_text)
            except ValueError:
                QMessageBox.warning(self, "خطأ", "السعر يجب أن يكون رقماً")
                return

        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(item_data['code']))
        self.table.setItem(row, 1, QTableWidgetItem(item_data['name']))
        self.table.setItem(row, 2, QTableWidgetItem(str(qty)))
        if self.op_type == "IN":
            self.table.setItem(row, 3, QTableWidgetItem(str(price)))

        self.items_to_move.append({
            "item_id": item_data['id'],
            "item_name": item_data['name'],
            "item_code": item_data['code'],
            "quantity": qty,
            "price": price
        })
        self.update_summary()

    def handle_submit(self):
        if not self.items_to_move:
            QMessageBox.warning(self, "تنبيه", "يرجى إضافة أصناف أولاً")
            return

        try:
            ref_no = self.controller.generate_invoice_no(self.op_type)
            self.ref_input.setText(ref_no)

            movement_data = {
                "reference_no": ref_no,
                "notes": "",
                "discount_percent": self.discount_input.value()
            }

            from utils.validator import Validator
            if self.op_type == "IN":
                if not Validator.is_not_empty(self.receiver_input.text()):
                    QMessageBox.warning(self, "تنبيه", "يرجى إدخال اسم المستلم")
                    return
                if not self.supplier_combo.currentData():
                    QMessageBox.warning(self, "تنبيه", "يرجى اختيار المورد")
                    return
                movement_data["supplier_id"] = self.supplier_combo.currentData()
                movement_data["received_by"] = self.receiver_input.text()
                self.controller.receive_stock(movement_data, self.items_to_move)
            else:
                if not Validator.is_not_empty(self.issuing_entity.text()) or \
                   not Validator.is_not_empty(self.receiver_name.text()):
                    QMessageBox.warning(self, "تنبيه", "يرجى إدخال الجهة المستلمة واسم الشخص")
                    return
                movement_data["issuing_entity"] = self.issuing_entity.text()
                movement_data["receiver_name"] = self.receiver_name.text()
                movement_data["reason"] = self.reason_input.text()
                self.controller.issue_stock(movement_data, self.items_to_move)

            QMessageBox.information(self, "نجاح", f"تمت العملية بنجاح. رقم الفاتورة: {ref_no}")
            self.reset_form()
        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "خطأ", f"فشل إتمام العملية: {str(e)}")

    def reset_form(self):
        self.ref_input.setText(self.controller.generate_invoice_no(self.op_type))
        self.table.setRowCount(0)
        self.items_to_move = []
        self.summary_label.setText("المجموع: 0.00 | الخصم: 0.00 | الإجمالي: 0.00")
        self.discount_input.setValue(0)
        if self.op_type == "IN":
            self.receiver_input.clear()
            if hasattr(self, 'price_input'): self.price_input.clear()
        else:
            self.issuing_entity.clear()
            self.receiver_name.clear()
            self.reason_input.clear()
