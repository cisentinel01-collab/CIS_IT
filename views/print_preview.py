from PySide6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel, QFrame, QHBoxLayout
from PySide6.QtCore import Qt
import os

class PrintPreviewDialog(QDialog):
    def __init__(self, pdf_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle("معاينة الفاتورة")
        self.resize(800, 600)
        self.pdf_path = pdf_path

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Header info
        header = QFrame()
        header.setStyleSheet("background-color: #1a2a6c; border-radius: 8px;")
        h_layout = QHBoxLayout(header)
        title = QLabel("تم توليد الملف بنجاح")
        title.setStyleSheet("color: #d4af37; font-size: 18px; font-weight: bold; padding: 10px;")
        h_layout.addWidget(title)
        layout.addWidget(header)

        # File path display
        path_frame = QFrame()
        path_frame.setObjectName("Card")
        p_layout = QVBoxLayout(path_frame)
        p_layout.addWidget(QLabel("مسار الملف:"))
        path_label = QLabel(pdf_path)
        path_label.setWordWrap(True)
        path_label.setStyleSheet("color: #1a2a6c; font-family: 'Courier New'; font-weight: bold;")
        p_layout.addWidget(path_label)
        layout.addWidget(path_frame)

        info_label = QLabel("يمكنك فتح الملف في متصفح النظام أو طباعته مباشرة.")
        info_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(info_label)

        layout.addStretch()

        # Action Buttons
        btn_layout = QHBoxLayout()

        open_btn = QPushButton("فتح في المستعرض")
        open_btn.setObjectName("GoldButton")
        open_btn.setMinimumHeight(45)
        open_btn.clicked.connect(self.open_file)
        btn_layout.addWidget(open_btn)

        close_btn = QPushButton("إغلاق")
        close_btn.setObjectName("PrimaryButton")
        close_btn.setMinimumHeight(45)
        close_btn.clicked.connect(self.accept)
        btn_layout.addWidget(close_btn)

        layout.addLayout(btn_layout)

    def open_file(self):
        if os.name == 'nt':
            os.startfile(self.pdf_path)
        else:
            os.system(f'open "{self.pdf_path}"')
