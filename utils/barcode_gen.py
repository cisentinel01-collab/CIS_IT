import barcode
from barcode.writer import ImageWriter
import os

class BarcodeGenerator:
    @staticmethod
    def generate(code, filename):
        try:
            EAN = barcode.get_barcode_class('code128')
            ean = EAN(code, writer=ImageWriter())
            # Ensure the directory exists
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            return ean.save(filename)
        except Exception as e:
            print(f"Barcode error: {e}")
            return None
