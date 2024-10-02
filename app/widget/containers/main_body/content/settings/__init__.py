from PySide2.QtWidgets import QTabWidget, QWidget

from .settings_tabs import SupportCenterTabContainer


class SettingsContainer(QTabWidget):
    def __init__(self, parent: QWidget, visible: bool = False):
        super().__init__(parent)
        self.support_center_tab_container = SupportCenterTabContainer(self)
        self.addTab(self.support_center_tab_container, "Ustawienia poradni")

        if not visible:
            self.setVisible(False)

    @property
    def support_center_data(self):
        return self.support_center_tab_container.support_center_data
