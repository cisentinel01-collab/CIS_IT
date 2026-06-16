from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QFrame, QGridLayout, QTableWidget, QTableWidgetItem, QHeaderView, QGroupBox)
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
            "monthly_ops": self.create_card("حركات الشهر", "0", "fa5s.calendar-alt", "#34495e"),
            "top_item": self.create_card("أكثر صنف صادر", "N/A", "fa5s.star", "#d35400")
        }

        keys = list(self.cards.keys())
        for i in range(len(keys)):
            grid_layout.addWidget(self.cards[keys[i]], i // 4, i % 4)

        self.main_layout.addLayout(grid_layout)

        # Lists Layout
        lists_layout = QHBoxLayout()

        # Low Stock List
        ls_group = QGroupBox("أصناف قاربت على النفاد")
        ls_layout = QVBoxLayout(ls_group)
        self.ls_table = QTableWidget()
        self.ls_table.setColumnCount(2)
        self.ls_table.setHorizontalHeaderLabels(["الصنف", "الكمية"])
        self.ls_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        ls_layout.addWidget(self.ls_table)
        lists_layout.addWidget(ls_group)

        # Top Suppliers List
        ts_group = QGroupBox("أهم الموردين")
        ts_layout = QVBoxLayout(ts_group)
        self.ts_table = QTableWidget()
        self.ts_table.setColumnCount(2)
        self.ts_table.setHorizontalHeaderLabels(["المورد", "عدد العمليات"])
        self.ts_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        ts_layout.addWidget(self.ts_table)
        lists_layout.addWidget(ts_group)

        self.main_layout.addLayout(lists_layout)

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
        self.cards["monthly_ops"]._value_label.setText(str(stats["monthly_ops"]))
        self.cards["value"]._value_label.setText(f"{stats['inventory_value']:,.2f}")
        self.cards["top_item"]._value_label.setText(str(stats["top_item"]))

        # Update Low Stock Table
        self.ls_table.setRowCount(0)
        for item in stats["low_stock_items"]:
            row = self.ls_table.rowCount()
            self.ls_table.insertRow(row)
            self.ls_table.setItem(row, 0, QTableWidgetItem(item['name']))
            self.ls_table.setItem(row, 1, QTableWidgetItem(str(item['current_stock'])))

        # Update Top Suppliers Table
        self.ts_table.setRowCount(0)
        for s in stats["top_suppliers"]:
            row = self.ts_table.rowCount()
            self.ts_table.insertRow(row)
            self.ts_table.setItem(row, 0, QTableWidgetItem(s['name']))
            self.ts_table.setItem(row, 1, QTableWidgetItem(str(s['op_count'])))

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
