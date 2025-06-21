from PySide6.QtWidgets import QFrame, QHBoxLayout, QPushButton, QWidget

from alinka.widget.actions import generate_and_save_decision


class ApplicationFooterContainer(QFrame):
    def __init__(self, parent: QWidget, visible: bool = False):
        super().__init__(parent)
        self.footer_container = parent
        layout = QHBoxLayout(self)
        layout.setContentsMargins(9, 9, 9, 9)
        self.print_btn = QPushButton("Drukuj dokumenty", self)
        self.print_btn.clicked.connect(self.print_documents)
        self.save_btn = QPushButton("Zapisz", self)
        self.save_btn.clicked.connect(self.save_document_data)
        layout.addWidget(self.print_btn)
        layout.addWidget(self.save_btn)

        self.setVisible(visible)

    @property
    def document_data(self):
        return self.footer_container.main_body_container.content_container.application_container.document_data

    def validate_document_data(self) -> None:
        content_container = self.footer_container.main_body_container.content_container
        if not content_container.validate_basic_settings():
            error_message = content_container.settings_container.error_message
            content_container.main_body_container.header_container.set_error_message(error_message)
            return
        if not content_container.validate_application():
            error_message = content_container.application_container.error_message
            content_container.main_body_container.header_container.set_error_message(error_message)
            return

    def print_documents(self) -> None:
        self.validate_document_data()
        generate_and_save_decision(form_data=self.document_data, generate=True)

    def save_document_data(self) -> None:
        content_container = self.footer_container.main_body_container.content_container
        application_container = content_container.application_container
        # Call validate_required_fields on the child tab
        if not application_container.child_tab_container.validate_required_fields():
            error_message = application_container.child_tab_container.error_message
            content_container.main_body_container.header_container.set_error_message(error_message)
            return
        self.validate_document_data()
        generate_and_save_decision(form_data=self.document_data, generate=False)
