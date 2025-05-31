from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGroupBox, QHBoxLayout

from alinka.widget.components import LabeledInputComponent


class GeneralDataGroupContainer(QGroupBox):
    def __init__(self, parent):
        super().__init__(title="Dane ogólne", parent=parent)
        layout = QHBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        self.decision_no = LabeledInputComponent("Numer orzeczenia", self)
        self.file_no = LabeledInputComponent("Numer teczki", self)
        layout.addWidget(self.decision_no)
        layout.addWidget(self.file_no)

    @property
    def is_valid(self) -> bool:
        return self.decision_no.is_valid and self.file_no.is_valid

    @property
    def error_message(self) -> str | None:
        for component in [self.decision_no, self.file_no]:
            if not component.is_valid:
                return component.error_message

        return None
