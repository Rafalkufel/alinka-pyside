from PySide2.QtWidgets import QFrame, QVBoxLayout, QWidget
from widget.containers.main_body.content.application import ApplicationContainer


class ContentContainer(QFrame):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(9, 9, 9, 9)
        self.application_container = ApplicationContainer(self)
        layout.addWidget(self.application_container)
