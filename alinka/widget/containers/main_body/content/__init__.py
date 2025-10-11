from PySide6.QtWidgets import QFrame, QVBoxLayout, QWidget

from alinka.widget.components import ValidationMixin

from .application import ApplicationContainer
from .browser import BrowserContainer
from .settings import SettingsContainer


class ContentContainer(ValidationMixin, QFrame):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.main_body_container = parent
        layout = QVBoxLayout(self)
        layout.setContentsMargins(9, 9, 9, 9)
        self.application_container = ApplicationContainer(self, visible=False)
        self.settings_container = SettingsContainer(self, visible=False)
        self.browser_container = BrowserContainer(self, visible=True)
        layout.addWidget(self.application_container)
        layout.addWidget(self.settings_container)
        layout.addWidget(self.browser_container)

    def validate_basic_settings(self) -> bool:
        header_container = self.main_body_container.header_container
        sidebar_menu_container = self.main_body_container.central_widget.side_bar.sidebar_menu_container
        if not self.settings_container.is_valid:
            error_message = self.settings_container.error_message
            header_container.set_error_message(error_message)
            sidebar_menu_container.toggle_create_application_btn(False)
            self.show_settings_container()
            return False
        else:
            header_container.clear_message()
            sidebar_menu_container.toggle_create_application_btn(True)
            return True

    def showEvent(self, event):
        self.validate_basic_settings()
        self.validate_application()
        return super().showEvent(event)

    def validate_application(self):
        if self.application_container.isVisible() and not self.application_container.is_valid:
            error_message = self.application_container.error_message
            self.main_body_container.header_container.set_error_message(error_message)
        else:
            self.main_body_container.header_container.clear_message()

    def show_settings_container(self):
        footer_container = self.main_body_container.footer_container
        self.application_container.setVisible(False)
        self.settings_container.setVisible(True)
        footer_container.show_settings_footer_container()
        self.browser_container.setVisible(False)

    def show_application_container(self):
        # before showing the application container, we need to validate the settings container
        if not self.validate_basic_settings():
            return
        self.settings_container.setVisible(False)
        self.application_container.setVisible(True)
        self.browser_container.setVisible(False)

    def show_browser_container(self):
        self.settings_container.setVisible(False)
        self.application_container.setVisible(False)
        self.browser_container.setVisible(True)
