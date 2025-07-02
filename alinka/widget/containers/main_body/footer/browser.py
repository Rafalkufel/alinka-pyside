from PySide6.QtWidgets import QFrame, QHBoxLayout, QPushButton, QWidget


class BrowserFooterContainer(QFrame):
    def __init__(self, parent: QWidget, visible: bool = False):
        super().__init__(parent)
        self.footer_container = parent
        layout = QHBoxLayout(self)
        layout.setContentsMargins(9, 9, 9, 9)
        self.create_new_btn = QPushButton("Utwórz nowy", self)
        self.create_new_btn.setEnabled(False)
        layout.addWidget(self.create_new_btn)

        self.setVisible(visible)
