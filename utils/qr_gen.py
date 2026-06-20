import qrcode
import os

class QRGenerator:
 @staticmethod
 def generate(data, filename=None):
 if not filename:
 filename = f"images/barcodes/QR_{data}.png"

 os.makedirs(os.path.dirname(filename), exist_ok=True)

 qr = qrcode.QRCode(version=1, box_size=10, border=5)
 qr.add_data(data)
 qr.make(fit=True)
 img = qr.make_image(fill_color="black", back_color="white")
 img.save(filename)
 return filename
