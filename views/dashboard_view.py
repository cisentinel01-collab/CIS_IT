from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QFrame, QGridLayout, QTableWidget, QTableWidgetItem, QHeaderView)
from PySide6.QtCore import Qt
import qtawesome as qta

class DashboardView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)

        # Stats Cards
        grid_layout = QGridLayout()
        self.cards = {
            "items": self.create_card("إجمالي الأصناف", "0", "fa5s.boxes", "#3498db"),
            "qty": self.create_card("إجمالي الكميات", "0", "fa5s.cubes", "#2ecc71"),
            "value": self.create_card("قيمة المخزون", "0", "fa5s.money-bill-wave", "#9b59b6"),
            "low_stock": self.create_card("أصناف منخفضة", "0", "fa5s.exclamation-triangle", "#e74c3c"),
            "suppliers": self.create_card("عدد الموردين", "0", "fa5s.truck", "#f1c40f"),
            "daily_ops": self.create_card("حركات اليوم", "0", "fa5s.exchange-alt", "#e67e22"),
            "pending_req": self.create_card("طلبات معلقة", "0", "fa5s.clock", "#34495e"),
            "users": self.create_card("المستخدمين", "0", "fa5s.users", "#16a085")
        }

        keys = list(self.cards.keys())
        for i in range(len(keys)):
            grid_layout.addWidget(self.cards[keys[i]], i // 4, i % 4)

        self.main_layout.addLayout(grid_layout)

        # Recent Activities Table
        activity_label = QLabel("آخر العمليات")
        activity_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #1a2a6c;")
        self.main_layout.addWidget(activity_label)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["التاريخ", "النوع", "الرقم المرجعي", "المورد/المستلم", "ملاحظات"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.main_layout.addWidget(self.table)

    def create_card(self, title, value, icon, color):
        card = QFrame()
        card.setObjectName("Card")
        layout = QHBoxLayout(card)

        info_layout = QVBoxLayout()
        title_label = QLabel(title)
        title_label.setObjectName("CardTitle")
        value_label = QLabel(value)
        value_label.setObjectName("CardValue")
        info_layout.addWidget(title_label)
        info_layout.addWidget(value_label)

        icon_label = QLabel()
        icon_label.setPixmap(qta.icon(icon, color=color).pixmap(40, 40))

        layout.addLayout(info_layout)
        layout.addStretch()
        layout.addWidget(icon_label)

        card._value_label = value_label # Store reference to update later
        return card

    def refresh(self):
        stats = self.controller.get_stats()
        self.cards["items"]._value_label.setText(str(stats["total_items"]))
        self.cards["qty"]._value_label.setText(str(stats["total_qty"]))
        self.cards["low_stock"]._value_label.setText(str(stats["low_stock_count"]))
        self.cards["suppliers"]._value_label.setText(str(stats["total_suppliers"]))
        self.cards["daily_ops"]._value_label.setText(str(stats["daily_ops"]))

        # Additional stats
        from database.db_manager import DBManager
        db = DBManager()
        val_res = db.execute_query("SELECT SUM(current_stock * COALESCE((SELECT price FROM movement_items WHERE item_id = items.id ORDER BY id DESC LIMIT 1), 0)) as val FROM items WHERE is_deleted = 0")
        self.cards["value"]._value_label.setText(f"{val_res[0]['val'] or 0:,.2f}")

        req_res = db.execute_query("SELECT COUNT(*) as count FROM purchase_requests WHERE status = 'pending' AND is_deleted = 0")
        self.cards["pending_req"]._value_label.setText(str(req_res[0]['count']))

        user_res = db.execute_query("SELECT COUNT(*) as count FROM users WHERE status != 'deleted'")
        self.cards["users"]._value_label.setText(str(user_res[0]['count']))

        # Update Table
        self.table.setRowCount(0)
        for m in stats["recent_movements"]:
            row = self.table.rowCount()
            self.table.insertRow(row)
            party = m['supplier_name'] if m['type'] == 'IN' else m['receiver_name']
            self.table.setItem(row, 0, QTableWidgetItem(m['date']))
            self.table.setItem(row, 1, QTableWidgetItem("وارد" if m['type'] == 'IN' else "صادر"))
            self.table.setItem(row, 2, QTableWidgetItem(m['reference_no']))
            self.table.setItem(row, 3, QTableWidgetItem(party or ""))
            self.table.setItem(row, 4, QTableWidgetItem(m['notes'] or ""))
