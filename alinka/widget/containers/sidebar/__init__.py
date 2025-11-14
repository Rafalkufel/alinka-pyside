from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QPushButton, QVBoxLayout, QWidget


class SidebarMenuContainer(QFrame):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.sidebar_menu = parent
        layout = QVBoxLayout(self)
        layout.setContentsMargins(9, 9, 9, 9)
        layout.setAlignment(Qt.AlignTop)
        self.search_child_btn = QPushButton("Wyszukaj", self)
        self.search_child_btn.clicked.connect(self.show_browser)
        layout.addWidget(self.search_child_btn)
        self.create_documents_btn = QPushButton("Utwórz dokument", self)
        self.create_documents_btn.clicked.connect(self.show_application)
        layout.addWidget(self.create_documents_btn)
        self.settings_btn = QPushButton("Ustawienia", self)
        self.settings_btn.clicked.connect(self.show_settings)
        layout.addWidget(self.settings_btn)

    @property
    def main_body(self):
        return self.sidebar_menu.central_widget.main_body

    def showEvent(self, event):
        self.main_body.content_container.validate_basic_settings()
        return super().showEvent(event)

    def show_browser(self):
        self.main_body.content_container.show_browser_container()
        self.main_body.footer_container.show_browser_footer_container()

    def show_application(self) -> None:
        if not self.main_body.content_container.validate_basic_settings():
            return None
        self.main_body.content_container.show_application_container()
        self.main_body.footer_container.show_application_footer_container()

    def show_settings(self) -> None:
        self.main_body.content_container.show_settings_container()
        self.main_body.footer_container.show_settings_footer_container()


class SidebarMenu(QFrame):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.central_widget = parent
        self.setFrameShape(QFrame.StyledPanel)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(9, 9, 9, 9)
        self.sidebar_menu_container = SidebarMenuContainer(self)
        layout.addWidget(self.sidebar_menu_container)
