from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QGroupBox, QHBoxLayout, QVBoxLayout

from alinka.constants.common import SchoolTypes
from alinka.db.queries import filter_schools_by_type
from alinka.schemas import DocumentData
from alinka.widget.components import (
    LabeledCheckboxComponent,
    LabeledComboBoxComponent,
    LabeledInputComponent,
    ValidationMixin,
)


class SchoolKlassProfessionFrame(ValidationMixin, QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.student_checkbox = LabeledCheckboxComponent("Uczeń", self)
        self.school_klass = LabeledInputComponent("Klasa", self)
        self.school_profession = LabeledInputComponent("Zawód", self)

        layout.addWidget(self.student_checkbox)
        layout.addWidget(self.school_klass)
        layout.addWidget(self.school_profession)


class SchoolDataGroupContainer(ValidationMixin, QGroupBox):
    def __init__(self, parent):
        super().__init__(title="Szkoła", parent=parent)
        self.child_data_container = parent
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)

        self.school_type = LabeledComboBoxComponent("Rodzaj Szkoły", self, 300, required=True, static=True)
        self.school_type.combobox.setPlaceholderText("Wybierz z listy...")
        self.school_type.combobox.addItems(SchoolTypes.values())
        self.school_type.combobox.currentTextChanged.connect(self.populate_school_combobox)

        self.school = LabeledComboBoxComponent("Szkoła", self, 300, required=True)
        self.school.combobox.setPlaceholderText("Wybierz szkołę...")

        self.school_klass_profession_frame = SchoolKlassProfessionFrame(self)
        self.student_checkbox = self.school_klass_profession_frame.student_checkbox
        self.school_klass = self.school_klass_profession_frame.school_klass
        self.school_profession = self.school_klass_profession_frame.school_profession

        layout.addWidget(self.school_type)
        layout.addWidget(self.school)
        layout.addWidget(self.school_klass_profession_frame)

        self.components = [
            self.school_type,
            self.school,
            self.student_checkbox,
            self.school_klass,
            self.school_profession,
        ]

    def populate_school_combobox(self):
        """On change selected school type we should clean item of school dropdown"""
        selected_school_type = self.school_type.combobox.currentText()
        self.school.combobox.clear()
        schools = filter_schools_by_type(selected_school_type)
        self.school.combobox.addItems([school.name for school in schools])

    def refresh_school_dropdown(self):
        """Refresh the school dropdown with latest schools from database"""
        current_school_type = self.school_type.combobox.currentText()
        if current_school_type:
            self.populate_school_combobox()

    def clear(self) -> None:
        self.school_type.combobox.clear()
        self.school.combobox.clear()
        self.school_type.combobox.addItems(SchoolTypes.values())
        self.student_checkbox.checkbox.setChecked(False)
        self.school_klass.clear()
        self.school_profession.clear()

    def populate_data(self, document_data: DocumentData) -> None:
        school_data = document_data.school
        child_data = document_data.child
        self.school_type.combobox.setCurrentText(school_data.type)
        self.school.combobox.setCurrentText(school_data.name)
        self.student_checkbox.checkbox.setChecked(child_data.student)
        self.school_klass.text = child_data.klass
        self.school_profession.text = child_data.profession

    @property
    def is_valid(self) -> bool:
        return all(c.is_valid for c in self.components)

    @property
    def error_message(self) -> str | None:
        for c in self.components:
            if not c.is_valid:
                return c.error_message

        return None

    def validate(self) -> bool:
        return all([c.validate() for c in self.components])

    def clear_validation_state(self) -> None:
        self.child_data_container.clear_validation_state()
