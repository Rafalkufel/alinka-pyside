from PySide2.QtWidgets import QTabWidget, QWidget

from .settings_tabs import SchoolTabContainer, SupportCenterTabContainer, TeamMemberTabContainer
from 


class SettingsContainer(QTabWidget):
    def __init__(self, parent: QWidget, visible: bool = False):
        super().__init__(parent)
        self.content_container = parent
        self.support_center_tab_container = SupportCenterTabContainer(self)
        self.schools_tab_container = SchoolTabContainer(self)
        self.team_member_tab_container = TeamMemberTabContainer(self)
        self.addTab(self.support_center_tab_container, "Dane poradni")
        self.addTab(self.schools_tab_container, "Szkoły")
        self.addTab(self.team_member_tab_container, "Zespół orzekający")

        if not visible:
            self.setVisible(False)

    @property
    def support_center_data(self):
        return self.support_center_tab_container.support_center_data
