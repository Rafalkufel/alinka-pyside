from PySide2.QtWidgets import QFrame, QVBoxLayout, QWidget
from widget.containers.main_body.content import ContentContainer
from widget.containers.main_body.footer import FooterContainer
from widget.containers.main_body.header import HeaderContainer


class MainBody(QFrame):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(9, 9, 9, 9)
        header_container = HeaderContainer(self)
        self.main_body_container = ContentContainer(self)
        footer_container = FooterContainer(self)
        layout.addWidget(header_container)
        layout.addWidget(self.main_body_container)
        layout.addWidget(footer_container)
