from PySide2.QtWidgets import QTabWidget, QWidget
from schemas import DocumentData, SupportCenterData
from widget.containers.main_body.content.application.application_tabs import (
    ApplicantsTabContainer,
    ApplicationTabContainer,
    ChildDataTabContainer,
    MeetingTabContainer,
)


class ApplicationContainer(QTabWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.id = None
        self.child_tab_container = ChildDataTabContainer(self)
        self.applicants_tab_container = ApplicantsTabContainer(self)
        self.application_tab_container = ApplicationTabContainer(self)
        self.meeting_tab_container = MeetingTabContainer(self)

        self.addTab(self.child_tab_container, "Uczeń")
        self.addTab(self.applicants_tab_container, "Wnioskodawcy")
        self.addTab(self.application_tab_container, "Wniosek")
        self.addTab(self.meeting_tab_container, "Zespół")

    @property
    def document_data(self) -> DocumentData:
        # to decide where we want to store static data like supoort center address
        # to refactor later
        support_center_data = SupportCenterData(
            address="pl. Słoneczna 620",
            town="Żywiec",
            postal_code="82-637",
            post=None,
            name_nominative="Miejska Poradnia Psychologiczno - Pedagogiczna w Wejherowo",
            name_genetive="Powiatowej Poradni Psychologiczno - Pedagogicznej w Ząbki",
            institute_name="Zespół Orzekający przy Powiatowej Poradni Psychologiczno - Pedagogicznej w Ząbki",
            kurator="Gdańsku, plac Wiśniowa 65/54, 66-804 Bielsko-Biała",
        )

        return DocumentData(
            id=1,
            file_no=self.child_tab_container.general_data_group.file_no.text,
            decision_no=self.child_tab_container.general_data_group.decision_no.text,
            child=self.child_tab_container.child_data,
            school=self.child_tab_container.school_data,
            applicants=self.applicants_tab_container.applicants,
            address_child_checkbox=self.applicants_tab_container.address_child_checkbox,
            address_first_parent_checkbox=self.applicants_tab_container.address_first_parent_checkbox,
            issue=self.application_tab_container.issue,
            period=self.application_tab_container.period,
            reasons=self.application_tab_container.reasons,
            activity_form=self.application_tab_container.activity_form,
            application_no=self.child_tab_container.general_data_group.decision_no.text,
            application_date=self.application_tab_container.application_date.date_input.date().toPython(),
            meeting_data=self.meeting_tab_container.meeting_data,
            support_center=support_center_data,
        )
