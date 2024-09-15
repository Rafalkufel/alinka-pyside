from PySide2.QtWidgets import QHBoxLayout, QMainWindow, QWidget
from widget.containers.main_body import MainBody
from widget.containers.sidebar import SidebarMenu


class CentralWidget(QWidget):
    def __init__(self, parent: QMainWindow):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(9, 9, 9, 9)
        side_bar = SidebarMenu(self)
        main_body = MainBody(self)
        layout.addWidget(side_bar)
        layout.addWidget(main_body)
