from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QGridLayout, QGroupBox, QWidget

from alinka.schemas import PersonalData
from alinka.widget.components import (
    LabeledCheckboxComponent,
    LabeledInputComponent,
    ValidationMixin,
)


class ParentAddressFrame(ValidationMixin, QFrame):
    def __init__(self, parent: QWidget, initial_height: int = 0):
        super().__init__(parent)
        self.applicant_frame = parent
        self.setFixedHeight(initial_height)

        layout = QGridLayout(self)
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(0, 0, 0, 0)
        self.address = LabeledInputComponent("Adres", self, required=True)
        self.town = LabeledInputComponent("Miejscowość", self, required=True)
        layout.addWidget(self.address, 0, 0)
        layout.addWidget(self.town, 0, 1)

        self.postal_code = LabeledInputComponent("Kod pocztowy", self, required=True)
        self.post = LabeledInputComponent("Poczta", self, required=True)
        layout.addWidget(self.postal_code, 1, 0)
        layout.addWidget(self.post, 1, 1)

        self.setLayout(layout)

        self.components = [self.address, self.town, self.postal_code, self.post]

    def clear(self) -> None:
        for component in self.components:
            component.clear()

    def populate_applicant_data(self, applicant_data: PersonalData) -> None:
        self.address.text = applicant_data.address
        self.town.text = applicant_data.town
        self.postal_code.text = applicant_data.postal_code
        self.post.text = applicant_data.post

    @property
    def is_valid(self) -> bool:
        return all(component.is_valid for component in self.components)

    @property
    def error_message(self) -> str | None:
        for component in self.components:
            if not component.is_valid:
                return component.error_message
        return None

    def validate(self) -> bool:
        return all([component.validate() for component in self.components])

    def clear_validation_state(self) -> None:
        self.applicant_frame.clear_validation_state()


class ApplicantDataGroup(ValidationMixin, QGroupBox):
    def __init__(self, title: str, parent: QWidget, checkbox_description: str, initial_height: int):
        super().__init__(title=title, parent=parent)
        self.applicants_tab_container = parent
        self.setFixedHeight(initial_height)
        layout = QGridLayout(self)
        layout.setAlignment(Qt.AlignTop)
        self.full_name = LabeledInputComponent("Imię i nazwisko", self, 200, required=True)
        self.full_name_gen = LabeledInputComponent("Imię i nazwisko (dopełniacz)", self, 200, required=True)
        layout.addWidget(self.full_name, 0, 0)
        layout.addWidget(self.full_name_gen, 0, 1)

        self.address_checkbox = LabeledCheckboxComponent(checkbox_description, self, "right")
        self.address_checkbox.checkbox.checkStateChanged.connect(self.show_hide_address_frame)
        layout.addWidget(self.address_checkbox, 1, 0)

        self.address_frame = ParentAddressFrame(self, 0)
        layout.addWidget(self.address_frame, 2, 0, 1, 2)

    @property
    def components(self) -> list[QFrame]:
        components = [self.full_name, self.full_name_gen]
        if self.address_checkbox.is_checked:
            components.extend(self.address_frame.components)
        return components

    def show_hide_address_frame(self) -> None:
        if self.address_checkbox.is_checked:
            self.setFixedHeight(220)
            self.address_frame.setFixedHeight(130)
        else:
            self.setFixedHeight(130)
            self.address_frame.setFixedHeight(0)
            self.address_frame.clear()

    @property
    def is_visible(self) -> bool:
        return self.height() > 0

    @is_visible.setter
    def is_visible(self, value: bool) -> None:
        if value:
            self.setFixedHeight(130)
            self.checkable = True
        else:
            self.clear()
            self.checkable = False
            self.setFixedHeight(0)

    def toggle(self) -> None:
        self.is_visible = not self.is_visible

    def populate_applicant_data(self, applicant_data: PersonalData) -> None:
        self.full_name.text = applicant_data.full_name
        self.full_name_gen.text = applicant_data.full_name_gen
        self.address_frame.populate_applicant_data(applicant_data)

    def clear(self) -> None:
        self.full_name.clear()
        self.full_name_gen.clear()
        self.address_checkbox.clear()
        self.address_frame.clear()

    @property
    def applicant_data(self) -> PersonalData | None:
        if self.full_name.text:
            return PersonalData(
                full_name=self.full_name.text,
                full_name_gen=self.full_name_gen.text,
                address=self.address_frame.address.text,
                town=self.address_frame.town.text,
                postal_code=self.address_frame.postal_code.text,
                post=self.address_frame.post.text,
            )

    @property
    def is_valid(self) -> bool:
        if not self.is_visible:
            return True
        return all(component.is_valid for component in self.components)

    @property
    def error_message(self) -> str | None:
        if not self.is_visible:
            return None

        for component in self.components:
            if not component.is_valid:
                return component.error_message

        return None

    def validate(self) -> bool:
        if not self.is_visible:
            return True
        return all([component.validate() for component in self.components])

    def clear_validation_state(self) -> None:
        self.applicants_tab_container.clear_validation_state()
