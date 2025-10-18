from PySide6.QtCore import QDate, Qt
from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtWidgets import (
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QListView,
    QVBoxLayout,
    QWidget,
)

from alinka.db.queries import get_team_members
from alinka.schemas import MeetingData, MeetingMemberData
from alinka.schemas.document_schema import DocumentData
from alinka.widget.components import (
    LabeledComboBoxComponent,
    LabeledDateComponent,
    LabeledInputComponent,
    ValidationMixin,
)


class MeetingDatetimeFrame(ValidationMixin, QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.meeting_date = LabeledDateComponent("Data zespołu", self)
        self.meeting_date.date_input.setDate(QDate.currentDate())
        self.meeting_time = LabeledInputComponent("Godzina zespołu", self)

        layout.addWidget(self.meeting_date)
        layout.addWidget(self.meeting_time)


class MeetingTabContainer(ValidationMixin, QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)

        self.meeting_member_group = QGroupBox("Członkowie zespołu", self)
        meeting_member_group_layout = QVBoxLayout(self.meeting_member_group)
        meeting_member_group_layout.setAlignment(Qt.AlignTop)
        self.model = QStandardItemModel()
        self.model.itemChanged.connect(self.item_changed)
        self.listView = QListView(self.meeting_member_group)

        self.populate_meeting_members()

        self.listView.setModel(self.model)
        meeting_member_group_layout.addWidget(self.listView)

        self.meeting_leader = LabeledComboBoxComponent("Przewodniczący zespołu", self)
        self.meeting_leader.combobox.setPlaceholderText("Wybierz z listy...")

        self.meeting_datetime_frame = MeetingDatetimeFrame(self)
        self.meeting_date = self.meeting_datetime_frame.meeting_date
        self.meeting_time = self.meeting_datetime_frame.meeting_time

        layout.addWidget(self.meeting_datetime_frame)
        layout.addWidget(self.meeting_member_group)
        layout.addWidget(self.meeting_leader)

    def populate_meeting_members(self, meeting_members: list[MeetingMemberData] | None = None) -> None:
        self.model.clear()
        for meeting_member_data in self.get_meeting_members_data():
            item = QStandardItem(meeting_member_data["name"])
            item.setData(meeting_member_data["id"])
            item.setCheckable(True)
            item.setCheckState(Qt.CheckState.Unchecked)
            self.model.appendRow(item)

    def showEvent(self, event):
        # this refreshes team members whenever tab is shown:
        self.model.clear()
        self.populate_meeting_members()

        return super().showEvent(event)

    def item_changed(self):
        self.meeting_leader.combobox.clear()
        for row_index in range(0, self.model.rowCount()):
            member = self.model.item(row_index)
            if member.checkState() == Qt.CheckState.Unchecked:
                continue
            self.meeting_leader.combobox.addItem(member.text(), member.data())

    def get_meeting_members_data(self) -> dict:
        return [tm.model_dump() for tm in get_team_members()]

    def get_meeting_member_by_id(self, meeting_member_id) -> MeetingMemberData:
        # To refactor. Maybe direct call to db?
        meeting_members_data = self.get_meeting_members_data()
        meeting_member = list(
            filter(lambda meeting_member: meeting_member["id"] == meeting_member_id, meeting_members_data)
        )[0]
        return MeetingMemberData(
            id=meeting_member["id"], name=meeting_member["name"], function=meeting_member["function"]
        )

    @property
    def meeting_data(self) -> MeetingData:
        meeting_members = list()
        for row_index in range(0, self.model.rowCount()):
            member = self.model.item(row_index)
            if member.checkState() == Qt.CheckState.Unchecked:
                continue
            meeting_member_data = self.get_meeting_member_by_id(member.data())
            if meeting_member_data.name == self.meeting_leader.combobox.currentText():
                meeting_members.insert(0, meeting_member_data)
            else:
                meeting_members.append(meeting_member_data)

        return MeetingData(
            members=meeting_members, date=self.meeting_date.date_input.date().toPython(), time=self.meeting_time.text
        )

    def clear(self):
        self.meeting_leader.remove_selection()
        self.meeting_leader.combobox.clear()
        self.meeting_date.date_input.setDate(QDate.currentDate())
        self.meeting_time.clear()
        self.model.clear()

    def populate_data(self, document_data: DocumentData) -> None:
        self.clear()
        meeting_data = document_data.meeting_data
        self.meeting_date.date_input.setDate(meeting_data.date)
        self.meeting_time.text = meeting_data.time
        self.populate_meeting_members(meeting_data.members)
        self.meeting_leader.combobox.setCurrentText(meeting_data.members[0].name)
