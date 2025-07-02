from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QGroupBox

from alinka.widget.components import LabeledInputComponent
from alinka.widget.validators import PeselValidator


class ChildDataGroupContainer(QGroupBox):
    def __init__(self, parent):
        super().__init__(title="Uczeń", parent=parent)
        layout = QGridLayout(self)
        layout.setAlignment(Qt.AlignTop)
        self.child_name_nom = LabeledInputComponent("Imię i nazwisko", self, 200)
        self.child_name_gen = LabeledInputComponent("Imię i nazwisko (dopełniacz)", self, 200)
        layout.addWidget(self.child_name_nom, 0, 0)
        layout.addWidget(self.child_name_gen, 0, 1)

        self.birth_place = LabeledInputComponent("Miejsce urodzenia", self)
        self.pesel_validator = PeselValidator()
        self.pesel = LabeledInputComponent("PESEL", self, validator=self.pesel_validator)
        self.pesel.line_edit.textChanged.connect(self.check_and_update_pesel_input)
        layout.addWidget(self.birth_place, 1, 0)
        layout.addWidget(self.pesel, 1, 1)

        self.address = LabeledInputComponent("Adres", self)
        self.town = LabeledInputComponent("Miejscowość", self)
        layout.addWidget(self.address, 2, 0)
        layout.addWidget(self.town, 2, 1)

        self.postal_code = LabeledInputComponent("Kod pocztowy", self)
        self.post = LabeledInputComponent("Poczta", self)
        layout.addWidget(self.postal_code, 3, 0)
        layout.addWidget(self.post, 3, 1)

    def check_and_update_pesel_input(self, pesel: str) -> None:
        state, _, _ = self.pesel_validator.validate(pesel, 0)
        if state == PeselValidator.Intermediate and len(pesel) >= 11:
            self.pesel.toggle_highlight("mistyrose")
        elif state == PeselValidator.Acceptable:
            self.pesel.toggle_highlight("lightgreen")
        else:
            self.pesel.toggle_highlight("")

    @property
    def is_valid(self) -> bool:
        return all(
            component.is_valid
            for component in [
                self.child_name_nom,
                self.child_name_gen,
                self.birth_place,
                self.pesel,
                self.address,
                self.town,
                self.postal_code,
                self.post,
            ]
        )

    @property
    def error_message(self) -> str | None:
        for component in [
            self.child_name_nom,
            self.child_name_gen,
            self.birth_place,
            self.pesel,
            self.address,
            self.town,
            self.postal_code,
            self.post,
        ]:
            if not component.is_valid:
                return component.error_message
        return None
