from PySide6.QtGui import QColor
from PySide6.QtWidgets import QTabWidget, QWidget

from alinka.constants.common import INVALID_FORM_MESSAGE
from alinka.db.queries import get_support_center_data
from alinka.schemas import DocumentData, SupportCenterData
from alinka.widget.components import ValidationMixin

from .application_tabs import (
    ApplicantsTabContainer,
    ApplicationTabContainer,
    ChildDataTabContainer,
    MeetingTabContainer,
)


class ApplicationContainer(ValidationMixin, QTabWidget):
    def __init__(self, parent: QWidget, visible: bool = False):
        super().__init__(parent)
        self.content_container = parent
        self.id = None

        self.child_tab_container = ChildDataTabContainer(self)
        self.applicants_tab_container = ApplicantsTabContainer(self)
        self.application_tab_container = ApplicationTabContainer(self)
        self.meeting_tab_container = MeetingTabContainer(self)

        self.addTab(self.child_tab_container, "Uczeń")
        self.addTab(self.applicants_tab_container, "Wnioskodawcy")
        self.addTab(self.application_tab_container, "Wniosek")
        self.addTab(self.meeting_tab_container, "Zespół")
        self.setCurrentIndex(0)

        self.previous_tab_index = self.currentIndex()
        self.currentChanged.connect(self.validate_previous_tab)

        self.setCurrentWidget(self.child_tab_container)
        self.setVisible(visible)

        self.containers = [
            self.child_tab_container,
            self.applicants_tab_container,
            self.application_tab_container,
            self.meeting_tab_container,
        ]

    @property
    def is_valid(self) -> bool:
        return all(tab.is_valid for tab in self.containers)

    @property
    def error_message(self) -> str | None:
        if not all(tab.is_valid for tab in self.containers):
            return INVALID_FORM_MESSAGE
        else:
            return None

    def clear_validation_state(self) -> None:
        self.tabBar().setTabTextColor(self.currentIndex(), QColor("black"))
        header_container = self.content_container.main_body_container.header_container
        header_container.clear_message()

    def validate_previous_tab(self, new_index: int) -> None:
        previous_tab = self.widget(self.previous_tab_index)
        if not previous_tab.validate():
            self.tabBar().setTabTextColor(self.previous_tab_index, QColor("red"))
            header_container = self.content_container.main_body_container.header_container
            header_container.set_error_message(INVALID_FORM_MESSAGE)
        else:
            self.tabBar().setTabTextColor(self.previous_tab_index, QColor("green"))
            self.clear_validation_state()

        self.previous_tab_index = new_index

    def finish_application_flow(self) -> None:
        """
        When application flow is finished (either by generating documents or cancelling)
        we should prepare the form for a new application.
        """
        self.clear()
        self.setCurrentWidget(self.child_tab_container)
        self.clear_validation_state()

    def validate(self) -> bool:
        if not all([tab.validate() for tab in self.containers]):
            for index, tab in enumerate(self.containers):
                if not tab.is_valid:
                    self.tabBar().setTabTextColor(index, QColor("red"))

            header_container = self.content_container.main_body_container.header_container
            header_container.set_error_message(self.error_message)
        else:
            self.clear_validation_state()
            return self.is_valid

    @property
    def document_data(self) -> DocumentData:
        support_center_data = get_support_center_data()
        support_center_data = SupportCenterData(**support_center_data.model_dump())

        return DocumentData(
            id=1,
            file_no=self.child_tab_container.general_data_group.file_no.text,
            decision_no=self.child_tab_container.general_data_group.decision_no.text,
            child=self.child_tab_container.child_data,
            school=self.child_tab_container.school_data,
            applicants=self.applicants_tab_container.applicants,
            is_first_parent_address_different=self.applicants_tab_container.is_first_parent_address_different,
            is_second_parent_address_different=self.applicants_tab_container.is_second_parent_address_different,
            issue=self.application_tab_container.issue,
            period=self.application_tab_container.period,
            reasons=self.application_tab_container.reasons,
            activity_form=self.application_tab_container.activity_form,
            application_no=self.child_tab_container.general_data_group.decision_no.text,
            application_date=self.application_tab_container.application_date.date_input.date().toPython(),
            meeting_data=self.meeting_tab_container.meeting_data,
            support_center=support_center_data,
        )

    def populate_application_form(self, document_data: DocumentData) -> None:
        self.child_tab_container.populate_data(document_data)
        self.applicants_tab_container.populate_data(document_data)

    def clear(self):
        self.child_tab_container.clear()
        self.applicants_tab_container.clear()
        self.application_tab_container.clear()
        self.meeting_tab_container.clear()
        self.id = None
