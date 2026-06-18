from PySide6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt
import os

class PrintPreviewDialog(QDialog):
    def __init__(self, pdf_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle("معاينة الطباعة")
        self.resize(900, 800)

        layout = QVBoxLayout(self)

        # In a real app we'd use a PDF viewer library or open in browser
        # For this demo, we'll just show the path and a button
        label = QLabel(f"تم توليد ملف PDF في:\n{pdf_path}")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        open_btn = QPushButton("فتح الملف")
        open_btn.clicked.connect(lambda: os.startfile(pdf_path) if os.name == 'nt' else os.system(f'open "{pdf_path}"'))
        layout.addWidget(open_btn)

        close_btn = QPushButton("إغلاق")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
