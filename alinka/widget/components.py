from PySide6.QtGui import QValidator
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDateEdit,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QVBoxLayout,
)

from alinka.widget.validators import RequiredValidator


class BaseComponent(QFrame):
    @property
    def is_valid(self) -> bool:
        """
        Method to check if the component is valid.
        If this method is not overridden in the subclass, component is always valid.
        """
        return True

    @property
    def error_message(self) -> str | None:
        """
        Method to get the error message if the component is not valid.
        If this method is not overridden in the subclass, it returns None.
        Return type should be string - if there's error message or None if there's no error.
        """
        return None


class LabeledInputComponent(BaseComponent):
    def __init__(
        self, text, parent, min_lenght: int | None = None, required: bool = False, validator: QValidator | None = None
    ):
        self.used_validator = None
        self.label = text
        self.is_required = required
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)
        label = QLabel(text=text, parent=self)
        self.line_edit = QLineEdit(self)
        if min_lenght:
            self.line_edit.setMinimumWidth(min_lenght)

        if validator:
            self.used_validator = validator
        elif required:
            self.used_validator = RequiredValidator()
        if self.used_validator:
            self.line_edit.setValidator(self.used_validator)
            self.line_edit.editingFinished.connect(self.validate)

        layout.addWidget(label)
        layout.addWidget(self.line_edit)

    @property
    def text(self) -> str:
        return self.line_edit.text()

    @text.setter
    def text(self, text):
        self.line_edit.setText(text)

    def clear(self) -> None:
        self.line_edit.clear()

    def toggle_highlight(self, color: str | None) -> None:
        if color:
            self.line_edit.setStyleSheet(f"background-color: {color};")
        else:
            self.line_edit.setStyleSheet("")

    def validate(self) -> None:
        if self.used_validator:
            validation_state, _, _ = self.used_validator.validate(self.text, 0)
            if validation_state != QValidator.Acceptable:
                self.toggle_highlight("mistyrose")
            else:
                self.toggle_highlight(None)

    @property
    def is_valid(self) -> bool:
        if not self.used_validator:
            return True

        validation_state, _, _ = self.used_validator.validate(self.text, 0)
        return validation_state == QValidator.Acceptable

    @property
    def error_message(self) -> str | None:
        if self.is_required and not self.text:
            return f"Pole '{self.label}' jest wymagane."
        if self.used_validator and not self.is_valid:
            return self.used_validator.default_error_message


class LabeledComboBoxComponent(BaseComponent):
    def __init__(self, text, parent, min_lenght: int | None = None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        label = QLabel(text=text, parent=self)
        self.combobox = QComboBox(self)
        if min_lenght:
            self.combobox.setMinimumWidth(min_lenght)
        layout.addWidget(label)
        layout.addWidget(self.combobox)


class LabeledCheckboxComponent(BaseComponent):
    def __init__(self, text, parent, label_position: str = "above"):
        super().__init__(parent)
        label = QLabel(text=text, parent=self)
        self.checkbox = QCheckBox(self)

        layout_class = QVBoxLayout if label_position == "above" else QHBoxLayout
        layout = layout_class(self)
        layout.addWidget(label)
        if label_position == "above":
            layout.insertWidget(1, self.checkbox)
        else:
            layout.addWidget(self.checkbox)


class LabeledDateComponent(BaseComponent):
    def __init__(self, text, parent):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        label = QLabel(text=text, parent=self)
        self.date_input = QDateEdit(self)
        self.date_input.setCalendarPopup(True)
        self.date_input.dateTime()
        layout.addWidget(label)
        layout.addWidget(self.date_input)
