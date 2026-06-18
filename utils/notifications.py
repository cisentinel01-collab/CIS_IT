from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QRect, QEasingCurve
import qtawesome as qta

class Notification(QWidget):
    def __init__(self, message, type="info", parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.ToolTip)
        self.setAttribute(Qt.WA_TranslucentBackground)

        layout = QVBoxLayout(self)
        self.frame = QWidget()
        self.frame.setObjectName("Notification")

        bg_color = "#1a2a6c" if type == "info" else "#27ae60" if type == "success" else "#c0392b"
        self.frame.setStyleSheet(f"""
            QWidget#Notification {{
                background-color: {bg_color};
                border-radius: 10px;
                padding: 15px;
            }}
            QLabel {{ color: white; font-weight: bold; font-size: 14px; }}
        """)

        frame_layout = QHBoxLayout(self.frame)
        icon = qta.icon("fa5s.info-circle" if type == "info" else "fa5s.check-circle", color="white")
        icon_label = QLabel()
        icon_label.setPixmap(icon.pixmap(24, 24))
        frame_layout.addWidget(icon_label)

        self.label = QLabel(message)
        frame_layout.addWidget(self.label)

        layout.addWidget(self.frame)

        self.timer = QTimer()
        self.timer.timeout.connect(self.close)
        self.timer.start(3000)

    @staticmethod
    def show_message(message, type="info", parent=None):
        notif = Notification(message, type, parent)
        # Position at top-right
        if parent:
            notif.move(parent.width() - 350, 50)
        notif.show()
