from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLineEdit, QPushButton,
                             QLabel, QFrame, QHBoxLayout, QMessageBox)
from PySide6.QtCore import Qt, Signal
import qtawesome as qta

class LoginView(QWidget):
    login_success = Signal(dict)

    def __init__(self, auth_controller):
        super().__init__()
        self.auth_controller = auth_controller
        self.setLayoutDirection(Qt.RightToLeft)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        container = QFrame()
        container.setFixedSize(400, 500)
        container.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 15px;
                border: 1px solid #dcdde1;
            }
        """)
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(40, 40, 40, 40)
        container_layout.setSpacing(20)

        # Logo/Icon
        logo_label = QLabel()
        logo_label.setPixmap(qta.icon("fa5s.ship", color="#1a2a6c").pixmap(80, 80))
        logo_label.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(logo_label)

        title = QLabel("American Marine Services")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #1a2a6c; border: none;")
        title.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(title)

        subtitle = QLabel("نظام إدارة المخازن")
        subtitle.setStyleSheet("font-size: 16px; color: #7f8c8d; border: none;")
        subtitle.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(subtitle)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("اسم المستخدم")
        self.username_input.setFixedHeight(40)
        container_layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("كلمة المرور")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedHeight(40)
        container_layout.addWidget(self.password_input)

        self.login_btn = QPushButton("تسجيل الدخول")
        self.login_btn.setObjectName("PrimaryButton")
        self.login_btn.setFixedHeight(45)
        self.login_btn.setCursor(Qt.PointingHandCursor)
        self.login_btn.clicked.connect(self.handle_login)
        container_layout.addWidget(self.login_btn)

        layout.addWidget(container)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            from utils.notifications import NotificationManager
            NotificationManager.show("يرجى إدخال اسم المستخدم وكلمة المرور", "warning")
            return

        success, user = self.auth_controller.login(username, password)
        if success:
            if user['status'] == 'disabled':
                QMessageBox.warning(self, "تنبيه", "هذا الحساب معطل. يرجى مراجعة المسؤول")
                return
            from utils.notifications import NotificationManager
            NotificationManager.show(f"تم تسجيل الدخول بنجاح. مرحباً {user['full_name']}", "success")
            self.login_success.emit(user)
        else:
            QMessageBox.critical(self, "خطأ", "اسم المستخدم أو كلمة المرور غير صحيحة")
