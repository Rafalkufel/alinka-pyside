from PySide2.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QWidget
from widget.actions import generate_and_save_decision


class FooterContainer(QFrame):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.parent = parent
        layout = QHBoxLayout(self)
        layout.setContentsMargins(9, 9, 9, 9)
        header_content = QLabel("Exemplary footer content", self)
        self.print_btn = QPushButton("Drukuj", self)
        self.print_btn.clicked.connect(self.print_documents)
        layout.addWidget(header_content)
        layout.addWidget(self.print_btn)

    def print_documents(self):
        document_data = self.parent.main_body_container.application_container.document_data
        generate_and_save_decision(form_data=document_data, generate=True)
