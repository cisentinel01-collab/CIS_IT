from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QLabel, QFrame)
from PySide6.QtCore import Qt
import qtawesome as qta

class DashboardView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # KPI Cards
        cards_layout = QGridLayout()
        self.stats = self.controller.get_dashboard_stats()

        self.total_items = self.create_card("إجمالي الأصناف", str(self.stats['total_items']), "fa5s.boxes")
        self.total_qty = self.create_card("إجمالي الكميات", str(self.stats['total_qty']), "fa5s.cubes")
        self.low_stock = self.create_card("أصناف منخفضة", str(self.stats['low_stock']), "fa5s.exclamation-triangle", "#c0392b")
        self.suppliers_count = self.create_card("عدد الموردين", str(self.stats['suppliers_count']), "fa5s.truck")

        cards_layout.addWidget(self.total_items, 0, 0)
        cards_layout.addWidget(self.total_qty, 0, 1)
        cards_layout.addWidget(self.low_stock, 0, 2)
        cards_layout.addWidget(self.suppliers_count, 0, 3)

        layout.addLayout(cards_layout)

        # Recent Activities
        recent_group = QFrame()
        recent_group.setObjectName("Card")
        recent_layout = QVBoxLayout(recent_group)
        recent_layout.addWidget(QLabel("آخر الحركات اليومية"))

        from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["الوقت", "النوع", "البيان", "بواسطة"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        activities = self.controller.get_recent_activities()
        for act in activities:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(act['timestamp']))
            self.table.setItem(row, 1, QTableWidgetItem(act['action']))
            self.table.setItem(row, 2, QTableWidgetItem(act['details'] or ""))
            self.table.setItem(row, 3, QTableWidgetItem(act['user_name']))

        recent_layout.addWidget(self.table)
        layout.addWidget(recent_group)

    def create_card(self, title, value, icon, color="#1a2a6c"):
        card = QFrame()
        card.setObjectName("Card")
        card_layout = QHBoxLayout(card)

        info_layout = QVBoxLayout()
        title_label = QLabel(title)
        title_label.setObjectName("CardTitle")
        val_label = QLabel(value)
        val_label.setObjectName("CardValue")
        val_label.setStyleSheet(f"color: {color};")
        info_layout.addWidget(title_label)
        info_layout.addWidget(val_label)

        card_layout.addLayout(info_layout)

        icon_label = QLabel()
        icon_label.setPixmap(qta.icon(icon, color=color).pixmap(40, 40))
        card_layout.addWidget(icon_label)

        return card
