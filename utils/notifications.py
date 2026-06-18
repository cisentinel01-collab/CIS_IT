from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QRect, QEasingCurve
import qtawesome as qta

class Notification(QWidget):
    def __init__(self, message, icon="fa5s.info-circle", color="#1a2a6c", parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.layout = QVBoxLayout(self)
        self.frame = QWidget()
        self.frame.setObjectName("NotificationFrame")
        self.frame.setStyleSheet(f"""
            #NotificationFrame {{
                background-color: white;
                border: 2px solid {color};
                border-radius: 10px;
            }}
            QLabel {{
                color: {color};
                font-weight: bold;
                font-size: 14px;
            }}
        """)

        frame_layout = QHBoxLayout(self.frame)

        icon_label = QLabel()
        icon_label.setPixmap(qta.icon(icon, color=color).pixmap(24, 24))
        frame_layout.addWidget(icon_label)

        msg_label = QLabel(message)
        frame_layout.addWidget(msg_label)

        self.layout.addWidget(self.frame)

        # Position and Animation
        self.adjustSize()
        if parent:
            self.start_pos = QRect(parent.width() - self.width() - 20, -100, self.width(), self.height())
            self.end_pos = QRect(parent.width() - self.width() - 20, 20, self.width(), self.height())
        else:
            self.start_pos = QRect(20, -100, self.width(), self.height())
            self.end_pos = QRect(20, 20, self.width(), self.height())

        self.setGeometry(self.start_pos)

        self.anim = QPropertyAnimation(self, b"geometry")
        self.anim.setDuration(500)
        self.anim.setStartValue(self.start_pos)
        self.anim.setEndValue(self.end_pos)
        self.anim.setEasingCurve(QEasingCurve.OutBack)

        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.hide_notification)

    def show_notification(self, duration=3000):
        self.show()
        self.anim.start()
        self.timer.start(duration)

    def hide_notification(self):
        self.anim.setDirection(QPropertyAnimation.Backward)
        self.anim.finished.connect(self.close)
        self.anim.start()

class NotificationManager:
    @staticmethod
    def success(parent, message):
        n = Notification(message, "fa5s.check-circle", "#27ae60", parent)
        n.show_notification()

    @staticmethod
    def error(parent, message):
        n = Notification(message, "fa5s.times-circle", "#e74c3c", parent)
        n.show_notification()

    @staticmethod
    def info(parent, message):
        n = Notification(message, "fa5s.info-circle", "#1a2a6c", parent)
        n.show_notification()
