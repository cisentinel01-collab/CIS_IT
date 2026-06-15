from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QStackedWidget, QFrame, QSpacerItem, QSizePolicy)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon
import qtawesome as qta

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("American Marine Services - WMS")
        self.resize(1200, 800)
        self.setLayoutDirection(Qt.RightToLeft)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.setup_sidebar()

        # Content Area
        self.content_area = QVBoxLayout()
        self.main_layout.addLayout(self.content_area)

        self.setup_header()

        self.stack = QStackedWidget()
        self.content_area.addWidget(self.stack)

    def setup_sidebar(self):
        self.sidebar = QFrame()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar_layout = QVBoxLayout(self.sidebar)

        # Logo placeholder
        logo_label = QLabel("AMS WMS")
        logo_label.setStyleSheet("color: #d4af37; font-size: 24px; font-weight: bold; margin: 20px; text-align: center;")
        self.sidebar_layout.addWidget(logo_label)

        self.nav_buttons = {}

        nav_items = [
            ("dashboard", "لوحة التحكم", "fa5s.tachometer-alt"),
            ("items", "الأصناف", "fa5s.boxes"),
            ("locations", "مواقع التخزين", "fa5s.map-marker-alt"),
            ("suppliers", "الموردين", "fa5s.truck"),
            ("stock_in", "وارد للمخزن", "fa5s.arrow-down"),
            ("stock_out", "صادر من المخزن", "fa5s.arrow-up"),
            ("requests", "طلبات الشراء", "fa5s.file-signature"),
            ("reports", "التقارير", "fa5s.chart-bar"),
            ("users", "المستخدمين", "fa5s.users-cog"),
            ("settings", "الإعدادات", "fa5s.cog")
        ]

        for key, text, icon_name in nav_items:
            btn = QPushButton(text)
            btn.setIcon(qta.icon(icon_name, color='white'))
            btn.setObjectName(f"nav_{key}")
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda checked, k=key: self.switch_view(k))
            self.sidebar_layout.addWidget(btn)
            self.nav_buttons[key] = btn

        self.sidebar_layout.addStretch()

        logout_btn = QPushButton("تسجيل الخروج")
        logout_btn.setIcon(qta.icon("fa5s.sign-out-alt", color='white'))
        logout_btn.clicked.connect(self.close) # Placeholder
        self.sidebar_layout.addWidget(logout_btn)

        self.main_layout.addWidget(self.sidebar)

    def setup_header(self):
        self.header = QFrame()
        self.header.setObjectName("Header")
        header_layout = QHBoxLayout(self.header)

        self.view_title = QLabel("لوحة التحكم")
        header_layout.addWidget(self.view_title)

        header_layout.addStretch()

        self.user_info = QLabel("مرحباً، مدير النظام")
        header_layout.addWidget(self.user_info)

        self.content_area.addWidget(self.header)

    def switch_view(self, key):
        # Update active button style
        for k, btn in self.nav_buttons.items():
            btn.setProperty("active", k == key)
            btn.style().unpolish(btn)
            btn.style().polish(btn)

        # Actual switching logic will be implemented later
        titles = {
            "dashboard": "لوحة التحكم",
            "items": "إدارة الأصناف",
            "locations": "إدارة مواقع التخزين",
            "suppliers": "إدارة الموردين",
            "stock_in": "عمليات الوارد",
            "stock_out": "عمليات الصادر",
            "requests": "إدارة طلبات الشراء",
            "reports": "التقارير والإحصائيات",
            "users": "إدارة المستخدمين",
            "settings": "إعدادات النظام"
        }
        self.view_title.setText(titles.get(key, ""))
