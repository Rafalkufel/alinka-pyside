from PySide6.QtWidgets import QFrame, QHBoxLayout, QPushButton, QWidget

from alinka.db.queries import create_school


class SettingsSchoolsContainer(QFrame):
    def __init__(self, parent: QWidget, visible: bool = False):
        super().__init__(parent)
        self.settings_footer_container = parent
        self.setVisible(visible)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(9, 9, 9, 9)

        add_remove_applicant_btn = QPushButton("Dodaj szkołę do listy")
        add_remove_applicant_btn.clicked.connect(self.add_school)
        layout.addWidget(add_remove_applicant_btn)

    def add_school(self):
        content_container = self.settings_footer_container.footer_container.main_body_container.content_container
        school_tab_container = content_container.settings_container.schools_tab_container

        create_school(
            school_tab_container.school_data_group.school_data.model_dump(exclude=("full_address", "description"))
        )
        school_tab_container.school_list.refresh()
