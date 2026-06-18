from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QLabel, QFrame, QTableWidget, QTableWidgetItem, QHeaderView, QProgressBar)
from PySide6.QtCore import Qt
import qtawesome as qta

class DashboardView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        stats = self.controller.get_dashboard_stats()

        # 1. KPI Cards Row
        cards_layout = QGridLayout()
        cards_layout.setSpacing(20)

        self.add_card(cards_layout, "إجمالي الأصناف", str(stats['total_items']), "fa5s.boxes", "#1a2a6c", 0, 0)
        self.add_card(cards_layout, "الكمية الإجمالية", str(stats['total_qty']), "fa5s.cubes", "#27ae60", 0, 1)
        self.add_card(cards_layout, "أصناف منخفضة", str(stats['low_stock']), "fa5s.exclamation-triangle", "#e74c3c", 0, 2)
        self.add_card(cards_layout, "عدد الموردين", str(stats['suppliers_count']), "fa5s.truck", "#f39c12", 0, 3)

        main_layout.addLayout(cards_layout)

        # 2. Middle Row: Charts/Progress & Recent Activity
        middle_layout = QHBoxLayout()
        middle_layout.setSpacing(20)

        # Left: Stock Status (Progress bars)
        stock_status_frame = QFrame()
        stock_status_frame.setObjectName("Card")
        ss_layout = QVBoxLayout(stock_status_frame)
        ss_title = QLabel("تنبيهات المخزون")
        ss_title.setObjectName("CardTitle")
        ss_layout.addWidget(ss_title)

        low_items = stats['stock_status'][:5] # Show top 5 low stock items
        if not low_items:
            ss_layout.addWidget(QLabel("المخزون مستقر"))
        else:
            for item in low_items:
                i_layout = QHBoxLayout()
                i_layout.addWidget(QLabel(item['name']))
                progress = QProgressBar()
                progress.setMaximum(item['min_stock'] * 2 if item['min_stock'] > 0 else 100)
                progress.setValue(item['current_stock'])
                progress.setFormat(f"{item['current_stock']} / {item['min_stock']}")
                progress.setStyleSheet("QProgressBar::chunk { background-color: #e74c3c; }")
                i_layout.addWidget(progress)
                ss_layout.addLayout(i_layout)

        ss_layout.addStretch()
        middle_layout.addWidget(stock_status_frame, 1)

        # Right: Recent Activity Table
        activity_frame = QFrame()
        activity_frame.setObjectName("Card")
        act_layout = QVBoxLayout(activity_frame)
        act_title = QLabel("آخر العمليات")
        act_title.setObjectName("CardTitle")
        act_layout.addWidget(act_title)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["الوقت", "المستخدم", "العملية"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setStyleSheet("border: none;")

        logs = self.controller.get_recent_activities()
        self.table.setRowCount(len(logs))
        for row, log in enumerate(logs):
            self.table.setItem(row, 0, QTableWidgetItem(log['timestamp'].split()[1] if ' ' in log['timestamp'] else log['timestamp']))
            self.table.setItem(row, 1, QTableWidgetItem(log['user_name'] or "النظام"))
            self.table.setItem(row, 2, QTableWidgetItem(log['action']))

        act_layout.addWidget(self.table)
        middle_layout.addWidget(activity_frame, 2)

        main_layout.addLayout(middle_layout)
        main_layout.addStretch()

    def add_card(self, layout, title, value, icon, color, r, c):
        card = QFrame()
        card.setObjectName("Card")
        card_layout = QHBoxLayout(card)

        icon_label = QLabel()
        icon_label.setPixmap(qta.icon(icon, color=color).pixmap(40, 40))
        card_layout.addWidget(icon_label)

        text_layout = QVBoxLayout()
        t_label = QLabel(title)
        t_label.setObjectName("CardTitle")
        v_label = QLabel(value)
        v_label.setObjectName("CardValue")
        v_label.setStyleSheet(f"color: {color};")

        text_layout.addWidget(t_label)
        text_layout.addWidget(v_label)
        card_layout.addLayout(text_layout)

        layout.addWidget(card, r, c)
