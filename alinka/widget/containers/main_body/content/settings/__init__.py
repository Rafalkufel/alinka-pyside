from PySide6.QtWidgets import QTabWidget, QWidget

from alinka.widget.components import ValidationMixin

from .settings_tabs import SupportCenterTabContainer


class SettingsContainer(ValidationMixin, QTabWidget):
    def __init__(self, parent: QWidget, visible: bool = False):
        super().__init__(parent)
        self.content_container = parent
        self.setVisible(visible)
        self.support_center_tab_container = SupportCenterTabContainer(self)
        self.addTab(self.support_center_tab_container, "Dane poradni")
        self.currentChanged.connect(self.handle_footer_visibility)

    @property
    def is_valid(self) -> bool:
        self.support_center_tab_container.is_valid

    @property
    def error_message(self) -> str | None:
        if not self.support_center_tab_container.is_valid:
            return self.support_center_tab_container.error_message

        return None

    @property
    def support_center_data(self):
        return self.support_center_tab_container.support_center_data

    def handle_footer_visibility(self, index):
        setting_footer_container = self.content_container.main_body_container.footer_container.settings_footer_container
        match index:
            case 0:
                setting_footer_container.show_footer_support_center_data_container()
