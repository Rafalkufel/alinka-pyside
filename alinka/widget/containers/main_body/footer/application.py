from PySide6.QtWidgets import (
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QMessageBox,
    QPushButton,
    QWidget,
)

from alinka.config import settings
from alinka.widget.actions import generate_and_save_decision


class ApplicationFooterContainer(QFrame):
    def __init__(self, parent: QWidget, visible: bool = False):
        super().__init__(parent)
        self.footer_container = parent
        layout = QHBoxLayout(self)
        layout.setContentsMargins(9, 9, 9, 9)
        self.cancel_btn = QPushButton("Anuluj", self)
        self.cancel_btn.clicked.connect(self.cancel_application)
        self.print_btn = QPushButton("Drukuj dokumenty", self)
        self.print_btn.clicked.connect(self.print_documents)
        layout.addWidget(self.cancel_btn)
        layout.addWidget(self.print_btn)

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
        content_container = self.footer_container.main_body_container.content_container
        application_container = content_container.application_container
        # Call validate_required_fields on the child tab
        if not application_container.validate():
            return
        self.validate_document_data()

        dialogTitle = "Wybierz katalog zapisu dokumentu"

        destination_path = QFileDialog.getExistingDirectory(self, dialogTitle, settings.DOCUMENTS_PATH)
        if not destination_path:
            return

        generate_and_save_decision(form_data=self.document_data, generate=True, destination_path=destination_path)
        content_container = self.footer_container.main_body_container.content_container
        content_container.main_body_container.header_container.set_success_message("Dokumenty zostały wygenerowane")
        content_container.show_browser_container()
        application_container.clear()
        application_container.setCurrentWidget(application_container.child_tab_container)
        self.footer_container.show_browser_footer_container()

    def cancel_application(self) -> None:
        reply = QMessageBox.question(
            self,
            "Potwierdzenie anulowania",
            "Czy na pewno chcesz anulować tworzenie dokumentu?\n\nWszystkie wprowadzone dane zostaną utracone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply != QMessageBox.StandardButton.Yes:
            return

        content_container = self.footer_container.main_body_container.content_container
        content_container.main_body_container.header_container.set_info_message("Tworzenie dokumentu anulowane")
        content_container.show_browser_container()
        application_container = content_container.application_container
        application_container.clear()
        application_container.setCurrentWidget(application_container.child_tab_container)
        self.footer_container.show_browser_footer_container()
