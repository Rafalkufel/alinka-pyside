from PySide6.QtGui import QValidator


class RequiredValidator(QValidator):
    default_error_message = "To pole jest wymagane"

    def validate(self, input_str: str, pos: int) -> tuple[QValidator.State, str, int]:
        if not input_str:
            return QValidator.Intermediate, input_str, pos
        return QValidator.Acceptable, input_str, pos


class PeselValidator(QValidator):
    default_error_message = "Nieprawidłowy PESEL"

    def validate(self, input_str: str, pos: int) -> tuple[QValidator.State, str, int]:
        if not input_str:
            return QValidator.Intermediate, input_str, pos
        if not input_str.isdigit():
            return QValidator.Invalid, input_str, pos
        if len(input_str) > 12:
            return QValidator.Invalid, input_str, pos

        if len(input_str) < 11:
            return QValidator.Intermediate, input_str, pos

        weights = [1, 3, 7, 9, 1, 3, 7, 9, 1, 3]
        digits = [int(ch) for ch in input_str]
        checksum = (10 - sum(w * d for w, d in zip(weights, digits)) % 10) % 10

        if checksum == digits[-1]:
            return QValidator.Acceptable, input_str, pos
        else:
            return QValidator.Intermediate, input_str, pos
