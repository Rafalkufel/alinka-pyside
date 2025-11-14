from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDateEdit,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QWidget,
)

from alinka import rspo_client
from alinka.constants.common import CHOOSE_FROM_LIST_MESSAGE


class ValidationMixin:
    """
    Mixin class to add validation functionality to components/containers
    Including this mixing ensures that all components/containers have a consistent
    interface for validation-related methods and properties.
    Method should be overridden in subclasses as needed.
    """

    @property
    def is_valid(self) -> bool:
        """Method to check if the component/container is valid."""
        return True

    @property
    def error_message(self) -> str | None:
        """
        Method to get the error message if the component is not valid.
        Return type should be string - if there's error message or None if there's no error.
        """
        return None

    def validate(self) -> bool:
        """
        Trigger validation of this component/containers and subclasses.
        This method should also update the visual state of the component/container
        to reflect whether it's valid or not (e.g., highlighting fields in red)
        by calling self.display_validation_result(validation_result)
        """
        is_valid = self.is_valid
        self.display_validation_result(is_valid)
        return is_valid

    def clear_validation_state(self) -> None:
        """Reset component and it's parent validation state"""
        pass

    def display_validation_result(self, validation_result: bool) -> None:
        """Display validation result by updating component's appearance"""
        pass


class LabeledInputComponent(ValidationMixin, QFrame):
    def __init__(
        self,
        text: str,
        parent: QWidget,
        min_length: int | None = None,
        required: bool = False,
    ):
        self.label = text
        self.is_required = required
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)
        label = QLabel(text=text, parent=self)
        self.line_edit = QLineEdit(self)
        if min_length:
            self.line_edit.setMinimumWidth(min_length)

        self.line_edit.textChanged.connect(self.clear_validation_state)

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

    def display_validation_result(self, validation_result: bool) -> None:
        if validation_result:
            self.toggle_highlight("lightgreen")
        else:
            self.toggle_highlight("mistyrose")

    def toggle_highlight(self, color: str | None) -> None:
        if color:
            self.line_edit.setStyleSheet(f"background-color: {color};")
        else:
            self.line_edit.setStyleSheet("")

    @property
    def is_valid(self) -> bool:
        if self.is_required:
            return bool(self.text.strip())
        return True

    @property
    def error_message(self) -> str | None:
        if self.is_required and not self.text:
            return f"Pole '{self.label}' jest wymagane."
        if self.used_validator and not self.is_valid:
            return self.used_validator.default_error_message

    def clear_validation_state(self) -> None:
        """Reset component and it's parent validation state"""
        self.parent().clear_validation_state()
        self.toggle_highlight(None)


class LabeledComboBoxComponent(ValidationMixin, QFrame):
    def __init__(
        self,
        text: str,
        parent: QWidget,
        min_length: int | None = None,
        required: bool = False,
        static: bool = False,
        unselectable: bool = False,
    ):
        self.label = text
        self.is_required = required
        # If static, options won't change dynamically, e.g. school types
        # clear means in this case remove selection only
        self.is_static = static
        # If unselectable, user is able to remove selection (set to no selection)
        self.is_unselectable = unselectable
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)
        label = QLabel(text=text, parent=self)
        self.combobox = QComboBox(self)
        if min_length:
            self.combobox.setMinimumWidth(min_length)
        if self.is_unselectable:
            self.combobox.insertItem(0, CHOOSE_FROM_LIST_MESSAGE)
            self.combobox.currentIndexChanged.connect(self._clear_if_unselected)
        self.combobox.currentIndexChanged.connect(self.clear_validation_state)
        self.combobox.currentTextChanged.connect(self.clear_validation_state)
        layout.addWidget(label)
        layout.addWidget(self.combobox)

    @property
    def text(self) -> str:
        return self.combobox.currentText()

    @text.setter
    def text(self, text):
        index = self.combobox.findText(text)
        if index >= 0:
            self.combobox.setCurrentIndex(index)

    def _clear_if_unselected(self) -> None:
        if self.is_unselectable and self.combobox.currentIndex() == 0:
            self.remove_selection()

    def remove_selection(self) -> None:
        self.combobox.setCurrentIndex(-1)

    def _insert_invitation_item(self) -> None:
        self.combobox.insertItem(0, CHOOSE_FROM_LIST_MESSAGE)

    def clear_options(self) -> None:
        self.combobox.clear()
        if self.is_unselectable:
            self._insert_invitation_item()

    def clear(self) -> None:
        self.remove_selection()
        if not self.is_static:
            self.clear_options()

    def addItems(self, items: list[str]) -> None:
        self.combobox.addItems(items)

    def display_validation_result(self, validation_result: bool) -> None:
        if validation_result:
            self.toggle_highlight("lightgreen")
        else:
            self.toggle_highlight("mistyrose")

    def toggle_highlight(self, color: str | None) -> None:
        if color:
            self.combobox.setStyleSheet(f"background-color: {color};")
        else:
            self.combobox.setStyleSheet(None)

    def clear_validation_state(self) -> None:
        """Reset component and it's parent validation state"""
        self.parent().clear_validation_state()
        self.toggle_highlight(None)

    @property
    def is_valid(self) -> bool:
        if not self.is_required:
            return True
        return bool(self.combobox.currentText())

    @property
    def error_message(self) -> str | None:
        if self.is_required and not self.text:
            return f"Pole '{self.label}' jest wymagane."
        return None


class LabeledCheckboxComponent(ValidationMixin, QFrame):
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

    def clear(self) -> None:
        self.checkbox.setChecked(False)

    @property
    def is_checked(self) -> bool:
        return self.checkbox.isChecked()


class LabeledDateComponent(ValidationMixin, QFrame):
    def __init__(self, text, parent, required: bool = False):
        super().__init__(parent)
        self.required = required
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        label = QLabel(text=text, parent=self)
        self.date_input = QDateEdit(self)
        self.date_input.setCalendarPopup(True)
        layout.addWidget(label)
        layout.addWidget(self.date_input)

    def clear(self) -> None:
        self.date_input.clear()

    def display_validation_result(self, validation_result: bool) -> None:
        if validation_result:
            self.toggle_highlight("lightgreen")
        else:
            self.toggle_highlight("mistyrose")

    def toggle_highlight(self, color: str | None) -> None:
        if color:
            self.date_input.setStyleSheet(f"background-color: {color};")
        else:
            self.date_input.setStyleSheet("")

    @property
    def is_valid(self) -> bool:
        if self.required and not self.date_input.date():
            return False
        return True

    @property
    def error_message(self) -> str | None:
        if not self.is_valid:
            return f"Pole '{self.label}' jest wymagane."

    def clear_validation_state(self) -> None:
        """Reset component and it's parent validation state"""
        self.parent().clear_validation_state()
        self.toggle_highlight(None)


class SelectProvinceDistrictGroup(ValidationMixin, QFrame):
    """Generic component to select provinece and district from RPSO"""

    selection_changed = Signal()

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.select_school_group = parent

        location_frame_layout = QHBoxLayout(self)
        location_frame_layout.setContentsMargins(0, 0, 0, 0)
        self.province_combobox = LabeledComboBoxComponent("Województwo", self, required=True)
        self.province_combobox.combobox.setPlaceholderText("Wybierz z listy...")
        self.province_combobox.combobox.currentTextChanged.connect(self.on_province_changed)

        provinces = rspo_client.list_provinces()
        for province in provinces:
            self.province_combobox.combobox.addItem(province.name, province.id)

        self.district_combobox = LabeledComboBoxComponent("Powiat", self, required=True)
        self.district_combobox.combobox.setPlaceholderText("Wybierz z listy...")
        self.district_combobox.combobox.currentTextChanged.connect(self.on_district_changed)
        location_frame_layout.addWidget(self.province_combobox)
        location_frame_layout.addWidget(self.district_combobox)

    @property
    def province_id(self) -> int | None:
        return self.province_combobox.combobox.currentData()

    @property
    def district_id(self) -> int | None:
        return self.district_combobox.combobox.currentData()

    def populate_districts_combobox(self) -> None:
        self.district_combobox.combobox.clear()
        if not self.province_id:
            return
        districts = rspo_client.list_districts(province_id=self.province_id)
        for district in districts:
            self.district_combobox.combobox.addItem(district.name, district.id)

    def on_province_changed(self):
        """
        In case of province change we should clear all other selections and
        repopulate districts combobox
        """
        self.selection_changed.emit()
        self.district_combobox.combobox.clear()
        self.populate_districts_combobox()

    def on_district_changed(self):
        """In case of district change we should only trigger selection changed signal"""
        self.selection_changed.emit()
