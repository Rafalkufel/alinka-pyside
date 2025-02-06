from PySide2.QtWidgets import QFrame, QHBoxLayout, QPushButton, QWidget


class SettingsTeamMembersContainer(QFrame):
    def __init__(self, parent: QWidget, visible: bool = False):
        super().__init__(parent)
        self.settings_footer_container = parent
        self.setVisible(visible)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(9, 9, 9, 9)

        self.add_new_member_btn = QPushButton("Dodaj", self)
        self.add_new_member_btn.clicked.connect(self.add_new_member)
        self.remove_selected_member_btn = QPushButton("Usuń", self)
        self.remove_selected_member_btn.setEnabled(False)
        self.remove_selected_member_btn.clicked.connect(self.remove_selected_member)
        self.save_team_members_btn = QPushButton("Zapisz", self)
        self.save_team_members_btn.clicked.connect(self.save_team_members)

        layout.addWidget(self.add_new_member_btn)
        layout.addWidget(self.remove_selected_member_btn)
        layout.addWidget(self.save_team_members_btn)

    def add_new_member(self):
        content_container = self.settings_footer_container.footer_container.main_body_container.content_container
        table_model = (
            content_container.settings_container.team_member_tab_container.team_members_table_group.table_model
        )
        if table_model.is_last_row_valid():
            table_model.append_new_team_member()

    def remove_selected_member(self):
        content_container = self.settings_footer_container.footer_container.main_body_container.content_container
        team_members_table_group = (
            content_container.settings_container.team_member_tab_container.team_members_table_group
        )
        table = team_members_table_group.table
        table_model = team_members_table_group.table_model
        selected_row = table.selectedIndexes()[0].row()
        table_model.remove_team_member(selected_row)

    def save_team_members(self):
        content_container = self.settings_footer_container.footer_container.main_body_container.content_container
        table_model = (
            content_container.settings_container.team_member_tab_container.team_members_table_group.table_model
        )
        table_model.save_team_member_list()

    @property
    def team_members(self):
        return self.parent.parent.content_container.settings_container.team_members
