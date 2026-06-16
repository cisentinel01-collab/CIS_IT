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
from controllers.user_controller import UserController

from views.login_view import LoginView
from views.main_window import MainWindow
from views.dashboard_view import DashboardView
from views.items_view import ItemsView
from views.suppliers_view import SuppliersView
from views.locations_view import LocationsView
from views.stock_operations_view import StockOperationsView
from views.user_management_view import UserManagementView
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
        self.user_controller = UserController()

        # Main UI
        self.main_window = MainWindow()
        self.login_view = LoginView(self.auth_controller)
        self.login_view.login_success.connect(self.on_login_success)

        self.setup_views()

        self.login_view.show()

    def init_database(self):
        db = DBManager()
        # Ensure migration V2 is applied
        from database.migrate import migrate
        migrate()

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

        # Connect refresh signals
        self.items_view.data_changed.connect(self.stock_in_view.load_items)
        self.items_view.data_changed.connect(self.stock_out_view.load_items)
        self.items_view.data_changed.connect(self.dashboard_view.refresh)

        self.suppliers_view.data_changed.connect(self.stock_in_view.load_suppliers)
        self.suppliers_view.data_changed.connect(self.dashboard_view.refresh)
        self.reports_view = ReportsView(self.report_controller)
        self.user_mgmt_view = UserManagementView(self.user_controller)
        self.settings_view = SettingsView()

        # Add to stack in main window
        self.main_window.stack.addWidget(self.dashboard_view) # 0
        self.main_window.stack.addWidget(self.items_view)     # 1
        self.main_window.stack.addWidget(self.locations_view) # 2
        self.main_window.stack.addWidget(self.suppliers_view) # 3
        self.main_window.stack.addWidget(self.stock_in_view)  # 4
        self.main_window.stack.addWidget(self.stock_out_view) # 5
        self.main_window.stack.addWidget(self.reports_view)   # 6
        self.main_window.stack.addWidget(self.user_mgmt_view) # 7
        self.main_window.stack.addWidget(self.settings_view)  # 8

        # Connect sidebar signals
        self.main_window.nav_buttons["dashboard"].clicked.connect(lambda: self.switch_to(0))
        self.main_window.nav_buttons["items"].clicked.connect(lambda: self.switch_to(1))
        self.main_window.nav_buttons["locations"].clicked.connect(lambda: self.switch_to(2))
        self.main_window.nav_buttons["suppliers"].clicked.connect(lambda: self.switch_to(3))
        self.main_window.nav_buttons["stock_in"].clicked.connect(lambda: self.switch_to(4))
        self.main_window.nav_buttons["stock_out"].clicked.connect(lambda: self.switch_to(5))
        self.main_window.nav_buttons["reports"].clicked.connect(lambda: self.switch_to(6))
        self.main_window.nav_buttons["users"].clicked.connect(lambda: self.switch_to(7))
        self.main_window.nav_buttons["settings"].clicked.connect(lambda: self.switch_to(8))

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
        elif index == 7:
            self.user_mgmt_view.refresh()

    def on_login_success(self, user):
        self.login_view.hide()
        full_name = user.get('full_name', 'مستخدم')
        self.main_window.user_info.setText(f"مرحباً، {full_name}")
        AuthManager.set_current_user(user)
        self.apply_permissions(user)
        self.dashboard_view.refresh()
        self.main_window.show()

    def apply_permissions(self, user):
        # Admin gets everything
        if user['role'] == 'admin':
            for btn in self.main_window.nav_buttons.values():
                btn.show()
            return

        # Granular permissions for others
        perms = self.user_controller.get_permissions(user['id'])
        for module, btn in self.main_window.nav_buttons.items():
            if module in perms:
                btn.setVisible(perms[module]['can_view'] == 1)
            else:
                # Default behavior for legacy or unspecified modules
                btn.hide()

    def run(self):
        sys.exit(self.app.exec())

if __name__ == "__main__":
    app = WMSApp()
    app.run()
