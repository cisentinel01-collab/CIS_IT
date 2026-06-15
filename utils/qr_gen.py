import qrcode
import os

class QRGenerator:
    @staticmethod
    def generate(data, filename):
        """Generates a QR code image."""
        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")

            # Ensure the directory exists
            os.makedirs(os.path.dirname(filename), exist_ok=True)

            img.save(f"{filename}.png")
            return f"{filename}.png"
        except Exception as e:
            print(f"QR generation error: {e}")
            return None

    @staticmethod
    def scan_mock(code):
        """Mock scanning logic if actual camera/scanner is not available."""
        # In a real app, this would use opencv-python or similar
        return code
