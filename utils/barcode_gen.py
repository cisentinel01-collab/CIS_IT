import barcode
from barcode.writer import ImageWriter
import os

class BarcodeGenerator:
    @staticmethod
    def generate(code, filename=None):
        if not filename:
            filename = f"images/barcodes/{code}"

        os.makedirs(os.path.dirname(filename), exist_ok=True)

        EAN = barcode.get_barcode_class('code128')
        ean = EAN(code, writer=ImageWriter())
        ean.save(filename)
        return f"{filename}.png"
