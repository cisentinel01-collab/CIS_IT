import re

class Validator:
    @staticmethod
    def is_numeric(text):
        """Checks if text contains only digits."""
        return bool(re.match(r'^\d+$', text))

    @staticmethod
    def is_alphabetic(text):
        """Checks if text contains only letters and spaces (including Arabic)."""
        # Arabic range: \u0600-\u06FF
        return bool(re.match(r'^[\u0600-\u06FFa-zA-Z\s]+$', text))

    @staticmethod
    def is_decimal(text):
        """Checks if text is a valid decimal number."""
        return bool(re.match(r'^\d+(\.\d+)?$', text))

    @staticmethod
    def setup_strict_validation(line_edit, type="text"):
        from PySide6.QtGui import QRegularExpressionValidator
        from PySide6.QtCore import QRegularExpression

        if type == "name":
            # Allow letters (Arabic/English), spaces, and basic symbols
            # Regex: allow anything except digits 0-9
            regex = QRegularExpression(r"^[^\d]*$")
            validator = QRegularExpressionValidator(regex, line_edit)
            line_edit.setValidator(validator)
        elif type == "phone":
            # Digits, plus, space, dash
            regex = QRegularExpression(r"^[0-9+\s-]*$")
            validator = QRegularExpressionValidator(regex, line_edit)
            line_edit.setValidator(validator)
            line_edit.setValidator(validator)
        elif type == "numeric":
            # Digits only
            regex = QRegularExpression(r"^\d*$")
            validator = QRegularExpressionValidator(regex, line_edit)
            line_edit.setValidator(validator)
        elif type == "decimal":
            # Decimal numbers
            regex = QRegularExpression(r"^\d*\.?\d*$")
            validator = QRegularExpressionValidator(regex, line_edit)
            line_edit.setValidator(validator)

    @staticmethod
    def is_not_empty(text):
        """Checks if text is not empty or just whitespace."""
        return bool(text and str(text).strip())

    @staticmethod
    def validate_password(password):
        """
        Password complexity: min 6 chars, at least one letter and one digit.
        """
        if len(password) < 6:
            return False, "كلمة المرور يجب أن تكون 6 أحرف على الأقل"
        if not any(c.isalpha() for c in password):
            return False, "كلمة المرور يجب أن تحتوي على حرف واحد على الأقل"
        if not any(c.isdigit() for c in password):
            return False, "كلمة المرور يجب أن تحتوي على رقم واحد على الأقل"
        return True, ""
