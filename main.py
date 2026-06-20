import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from views.login_view import LoginView
from database.migrate import migrate

def main():
 # Ensure necessary directories exist
 for d in ["reports", "backups", "images/barcodes", "logo"]:
 os.makedirs(d, exist_ok=True)

 # Run database migration
 try:
 migrate()
 except Exception as e:
 print(f"Migration error: {e}")

 app = QApplication(sys.argv)
 app.setLayoutDirection(Qt.RightToLeft)

 # Load Styles
 try:
 with open("assets/styles.qss", "r", encoding="utf-8") as f:
 app.setStyleSheet(f.read())
 except Exception as e:
 print(f"Style loading error: {e}")

 login = LoginView()
 login.show()

 sys.exit(app.exec())

if __name__ == "__main__":
 main()
