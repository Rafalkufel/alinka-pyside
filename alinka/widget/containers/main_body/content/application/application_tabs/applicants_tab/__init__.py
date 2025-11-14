from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton, QVBoxLayout, QWidget

from alinka.schemas import DocumentData, PersonalData
from alinka.widget.components import ValidationMixin

from .applicant_data_group import ApplicantDataGroup


class ApplicantsTabContainer(ValidationMixin, QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.application_container = parent
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(0, 0, 0, 0)
        self.applicant_1_data_group = ApplicantDataGroup(
            title="Wnioskodawca 1", parent=self, checkbox_description="Adres inny niż dziecka", initial_height=130
        )
        self.applicant_2_data_group = ApplicantDataGroup(
            title="Wnioskodawca 2",
            parent=self,
            checkbox_description="Adres inny niż pierwszego rodzica",
            initial_height=0,
        )
        add_remove_applicant_btn = QPushButton("Dodaj/usuń wnioskodawcę")
        add_remove_applicant_btn.clicked.connect(self.applicant_2_data_group.toggle)
        layout.addWidget(self.applicant_1_data_group)
        layout.addWidget(self.applicant_2_data_group)
        layout.addWidget(add_remove_applicant_btn)

        self.containers = [self.applicant_1_data_group, self.applicant_2_data_group]

    @property
    def applicants(self) -> list[PersonalData]:
        return [applicant.applicant_data for applicant in self.containers if applicant.applicant_data]

    @property
    def is_first_parent_address_different(self) -> bool:
        return self.applicant_1_data_group.address_checkbox.is_checked

    @property
    def is_second_parent_address_different(self) -> bool:
        return self.applicant_2_data_group.address_checkbox.is_checked

    @property
    def is_second_applicant_active(self) -> bool:
        return self.applicant_2_data_group.is_visible

    def clear(self) -> None:
        self.applicant_1_data_group.clear()
        self.applicant_2_data_group.clear()

    def populate_data(self, document_data: DocumentData) -> None:
        applicants = document_data.applicants
        checkbox1 = document_data.is_first_parent_address_different
        checkbox2 = document_data.is_second_parent_address_different

        if len(applicants) == 1:
            self.applicant_1_data_group.populate_applicant_data(applicants[0])
            self.applicant_1_data_group.address_checkbox.checkbox.setChecked(checkbox1)
            self.applicant_2_data_group.clear()
            self.applicant_2_data_group.checkable = False
            self.applicant_2_data_group.setFixedHeight(0)
        elif len(applicants) == 2:
            self.applicant_1_data_group.populate_applicant_data(applicants[0])
            self.applicant_2_data_group.populate_applicant_data(applicants[1])
            self.applicant_1_data_group.address_checkbox.checkbox.setChecked(checkbox1)
            self.applicant_2_data_group.address_checkbox.checkbox.setChecked(checkbox2)
            self.applicant_2_data_group.setFixedHeight(200)

    @property
    def is_valid(self) -> bool:
        return all(applicant.is_valid for applicant in self.containers if applicant.is_visible)

    def error_messages(self) -> str | None:
        for applicant in self.containers:
            if applicant.is_visible and not applicant.is_valid:
                return applicant.error_message

        return None

    def validate(self) -> bool:
        return all([a.validate() for a in self.containers if a.is_visible])

    def clear_validation_state(self) -> None:
        self.application_container.clear_validation_state()
