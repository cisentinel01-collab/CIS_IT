from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QApplication
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QRect, QEasingCurve, QPoint
from PySide6.QtGui import QColor, QFont
import qtawesome as qta

class NotificationWidget(QWidget):
    def __init__(self, message, type="info", parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.layout = QHBoxLayout(self)
        self.bg_frame = QWidget()
        self.bg_frame.setObjectName("NotificationFrame")

        colors = {
            "success": "#2ecc71",
            "warning": "#f1c40f",
            "error": "#e74c3c",
            "info": "#3498db"
        }
        icons = {
            "success": "fa5s.check-circle",
            "warning": "fa5s.exclamation-triangle",
            "error": "fa5s.times-circle",
            "info": "fa5s.info-circle"
        }

        self.bg_frame.setStyleSheet(f"""
            QWidget#NotificationFrame {{
                background-color: {colors.get(type, "#3498db")};
                border-radius: 10px;
                color: white;
            }}
        """)

        frame_layout = QHBoxLayout(self.bg_frame)

        icon_label = QLabel()
        icon_label.setPixmap(qta.icon(icons.get(type, "fa5s.info-circle"), color="white").pixmap(24, 24))
        frame_layout.addWidget(icon_label)

        msg_label = QLabel(message)
        msg_label.setStyleSheet("color: white; font-weight: bold; font-size: 14px; border: none;")
        frame_layout.addWidget(msg_label)

        self.layout.addWidget(self.bg_frame)

        # Position at top right
        self.resize(300, 60)

    def show_animated(self):
        screen = QApplication.primaryScreen().geometry()
        start_pos = QPoint(screen.width(), 50)
        end_pos = QPoint(screen.width() - 320, 50)

        self.move(start_pos)
        self.show()

        self.anim = QPropertyAnimation(self, b"pos")
        self.anim.setDuration(500)
        self.anim.setStartValue(start_pos)
        self.anim.setEndValue(end_pos)
        self.anim.setEasingCurve(QEasingCurve.OutCubic)
        self.anim.start()

        QTimer.singleShot(3000, self.hide_animated)

    def hide_animated(self):
        screen = QApplication.primaryScreen().geometry()
        end_pos = QPoint(screen.width(), 50)

        self.anim = QPropertyAnimation(self, b"pos")
        self.anim.setDuration(500)
        self.anim.setStartValue(self.pos())
        self.anim.setEndValue(end_pos)
        self.anim.setEasingCurve(QEasingCurve.InCubic)
        self.anim.finished.connect(self.close)
        self.anim.start()

class NotificationManager:
    @staticmethod
    def show(message, type="info"):
        # Sound effects would be played here if enabled in settings
        # from utils.sound_player import SoundPlayer
        # if settings.sounds_enabled: SoundPlayer.play(type)

        notif = NotificationWidget(message, type)
        notif.show_animated()
        # We need to keep a reference or the widget might be garbage collected
        if not hasattr(NotificationManager, '_notifications'):
            NotificationManager._notifications = []
        NotificationManager._notifications.append(notif)
        notif.destroyed.connect(lambda: NotificationManager._notifications.remove(notif))
