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
        self.setFixedHeight(initial_height)

        layout = QGridLayout(self)
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(0, 0, 0, 0)
        self.address = LabeledInputComponent("Adres", self)
        self.town = LabeledInputComponent("Miejscowość", self)
        layout.addWidget(self.address, 0, 0)
        layout.addWidget(self.town, 0, 1)

        self.postal_code = LabeledInputComponent("Kod pocztowy", self)
        self.post = LabeledInputComponent("Poczta", self)
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


class ApplicantDataGroup(ValidationMixin, QGroupBox):
    def __init__(self, title: str, parent: QWidget, checkbox_description: str, initial_height: int):
        super().__init__(title=title, parent=parent)
        self.setFixedHeight(initial_height)
        layout = QGridLayout(self)
        layout.setAlignment(Qt.AlignTop)
        self.full_name = LabeledInputComponent("Imię i nazwisko", self, 200)
        self.full_name_gen = LabeledInputComponent("Imię i nazwisko (dopełniacz)", self, 200)
        layout.addWidget(self.full_name, 0, 0)
        layout.addWidget(self.full_name_gen, 0, 1)

        self.address_checkbox = LabeledCheckboxComponent(checkbox_description, self, "right")
        self.address_checkbox.checkbox.checkStateChanged.connect(self.show_hide_address_frame)
        layout.addWidget(self.address_checkbox, 1, 0)

        self.address_frame = ParentAddressFrame(self, 0)
        layout.addWidget(self.address_frame, 2, 0, 1, 2)

    def show_hide_address_frame(self) -> None:
        if self.address_checkbox.checkbox.isChecked():
            self.setFixedHeight(220)
            self.address_frame.setFixedHeight(130)
        else:
            self.setFixedHeight(130)
            self.address_frame.setFixedHeight(0)
            self.address_frame.clear()

    def populate_applicant_data(self, applicant_data: PersonalData) -> None:
        self.full_name.text = applicant_data.full_name
        self.full_name_gen.text = applicant_data.full_name_gen
        self.address_frame.populate_applicant_data(applicant_data)

    def clear(self) -> None:
        self.full_name.clear()
        self.full_name_gen.clear()
        self.address_checkbox.checkbox.setChecked(False)
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
