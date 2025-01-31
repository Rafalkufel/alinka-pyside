from PySide2.QtWidgets import QVBoxLayout, QWidget

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QFrame, QGroupBox, QHBoxLayout, QVBoxLayout, QWidget, QPushButton
from widget.components import LabeledComboBoxComponent, LabeledInputComponent

from app import rspo_client
from app.constants.common import RPSO_SUPPORT_CENTER_TYPE_ID
from app.schemas.rspo_schema import InstitutionRequestBody


class TeamMemberTableGroup(QGroupBox):
    def __init__(self, parent: QWidget):
        super().__init__(title="Członkowie zespołu orzekającego", parent=parent)
        self.parent = parent
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)


class TeamMemberDataGroup(QGroupBox):
    def __init__(self, parent: QWidget):
        super().__init__(title="Dane nauczyciela", parent=parent)
        self.parent = parent
        layout = QVBoxLayout(self)
        
        team_member_data = QFrame(parent=self)
        team_member_layout = QHBoxLayout(team_member_data)
        team_member_layout.setAlignment(Qt.AlignTop)
        team_member_name = LabeledInputComponent("Imię i nazwisko członka", parent=team_member_data)
        team_member_role = LabeledInputComponent("specjalność", parent=team_member_data)
        team_member_layout.addWidget(team_member_name)
        team_member_layout.addWidget(team_member_role)
        
        save_button = QPushButton(text="Zapisz", parent=self)
        
        layout.addWidget(team_member_data)
        layout.addWidget(save_button)


class TeamMemberTabContainer(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        self.team_members_table_group = TeamMemberTableGroup(self)
        self.team_member_data_group = TeamMemberDataGroup(self)
        
        
    #     self.select_support_center_group = SelectSupportCenterGroup(self)
    #     self.support_center_data_group = SupportCenterDataGroup(self)
        layout.addWidget(self.team_members_table_group)
        layout.addWidget(self.team_member_data_group)

    # @property
    # def support_center_data(self):
    #     return self.support_center_data_group.support_center_data