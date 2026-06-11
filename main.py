import sys
import os
from PySide6.QtWidgets import QApplication, QStackedWidget
from PySide6.QtCore import Qt

from database.db_manager import DBManager
from models.user import User
from utils.auth import AuthManager
from controllers.auth_controller import AuthController
from controllers.dashboard_controller import DashboardController
from controllers.item_controller import ItemController
from controllers.supplier_controller import SupplierController
from controllers.stock_controller import StockController
from controllers.report_controller import ReportController

from views.login_view import LoginView
from views.main_window import MainWindow
from views.dashboard_view import DashboardView
from views.items_view import ItemsView
from views.suppliers_view import SuppliersView
from views.locations_view import LocationsView
from views.stock_operations_view import StockOperationsView
from views.reports_view import ReportsView
from views.settings_view import SettingsView

class WMSApp:
    def __init__(self):
        self.app = QApplication(sys.argv)

        # Load Styles
        with open("assets/styles.qss", "r") as f:
            self.app.setStyleSheet(f.read())

        self.init_database()

        # Controllers
        self.auth_controller = AuthController()
        self.dashboard_controller = DashboardController()
        self.item_controller = ItemController()
        self.supplier_controller = SupplierController()
        self.stock_controller = StockController()
        self.report_controller = ReportController()

        # Main UI
        self.main_window = MainWindow()
        self.login_view = LoginView(self.auth_controller)
        self.login_view.login_success.connect(self.on_login_success)

        self.setup_views()

        self.login_view.show()

    def init_database(self):
        db = DBManager()
        user_model = User()
        # Create default admin if not exists
        if not user_model.get_by_username("admin"):
            hashed = AuthManager.hash_password("admin123")
            user_model.create_user("admin", hashed, "المدير العام", "admin")

        # Create other roles for demonstration
        if not user_model.get_by_username("keeper"):
            hashed = AuthManager.hash_password("keeper123")
            user_model.create_user("keeper", hashed, "أمين المخزن", "warehouse_keeper")

        if not user_model.get_by_username("supervisor"):
            hashed = AuthManager.hash_password("super123")
            user_model.create_user("supervisor", hashed, "المشرف", "supervisor")

    def setup_views(self):
        # Create view instances
        from models.location import Location
        self.location_model = Location()
        self.dashboard_view = DashboardView(self.dashboard_controller)
        self.items_view = ItemsView(self.item_controller)
        self.locations_view = LocationsView(self.location_model)
        self.suppliers_view = SuppliersView(self.supplier_controller)
        self.stock_in_view = StockOperationsView(self.stock_controller, "IN")
        self.stock_out_view = StockOperationsView(self.stock_controller, "OUT")
        self.reports_view = ReportsView(self.report_controller)
        self.settings_view = SettingsView()

        # Add to stack in main window
        self.main_window.stack.addWidget(self.dashboard_view) # Index 0
        self.main_window.stack.addWidget(self.items_view)     # Index 1
        self.main_window.stack.addWidget(self.locations_view) # Index 2
        self.main_window.stack.addWidget(self.suppliers_view) # Index 3
        self.main_window.stack.addWidget(self.stock_in_view)  # Index 4
        self.main_window.stack.addWidget(self.stock_out_view) # Index 5
        self.main_window.stack.addWidget(self.reports_view)   # Index 6
        self.main_window.stack.addWidget(self.settings_view)  # Index 7

        # Connect sidebar signals
        self.main_window.nav_buttons["dashboard"].clicked.connect(lambda: self.switch_to(0))
        self.main_window.nav_buttons["items"].clicked.connect(lambda: self.switch_to(1))
        self.main_window.nav_buttons["locations"].clicked.connect(lambda: self.switch_to(2))
        self.main_window.nav_buttons["suppliers"].clicked.connect(lambda: self.switch_to(3))
        self.main_window.nav_buttons["stock_in"].clicked.connect(lambda: self.switch_to(4))
        self.main_window.nav_buttons["stock_out"].clicked.connect(lambda: self.switch_to(5))
        self.main_window.nav_buttons["reports"].clicked.connect(lambda: self.switch_to(6))
        self.main_window.nav_buttons["settings"].clicked.connect(lambda: self.switch_to(7))

    def switch_to(self, index):
        self.main_window.stack.setCurrentIndex(index)
        # Refresh current view if needed
        if index == 0:
            self.dashboard_view.refresh()
        elif index == 1:
            self.items_view.refresh()
        elif index == 2:
            self.locations_view.refresh()
        elif index == 3:
            self.suppliers_view.refresh()

    def on_login_success(self, user):
        self.login_view.hide()
        self.main_window.user_info.setText(f"مرحباً، {user['full_name']}")
        self.apply_permissions(user['role'])
        self.dashboard_view.refresh()
        self.main_window.show()

    def apply_permissions(self, role):
        # Role-based UI visibility
        if role == 'warehouse_keeper':
            self.main_window.nav_buttons["reports"].hide()
            self.main_window.nav_buttons["settings"].hide()
        elif role == 'supervisor':
            self.main_window.nav_buttons["items"].hide()
            self.main_window.nav_buttons["suppliers"].hide()
            self.main_window.nav_buttons["stock_in"].hide()
            self.main_window.nav_buttons["stock_out"].hide()
            self.main_window.nav_buttons["settings"].hide()

    def run(self):
        sys.exit(self.app.exec())

if __name__ == "__main__":
    app = WMSApp()
    app.run()
