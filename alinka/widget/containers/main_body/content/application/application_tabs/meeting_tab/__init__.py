from PySide6.QtCore import QDate, Qt, Signal
from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtWidgets import (
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QListView,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from alinka.db.queries import (
    delete_team_member,
    get_meeting_member_by_id,
    get_team_members,
    insert_team_member,
    update_team_member,
)
from alinka.schemas import (
    MeetingData,
    MeetingMemberData,
    TeamMemberDbCreateSchema,
    TeamMemberDbSchema,
)
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

        self.meeting_date = LabeledDateComponent("Data zespołu", self, required=True)
        self.meeting_date.date_input.setDate(QDate.currentDate())
        self.meeting_time = LabeledInputComponent("Godzina zespołu", self, required=True)

        layout.addWidget(self.meeting_date)
        layout.addWidget(self.meeting_time)

    @property
    def is_valid(self) -> bool:
        return self.meeting_date.is_valid and self.meeting_time.is_valid

    @property
    def error_message(self) -> str | None:
        for c in [self.meeting_date, self.meeting_time]:
            if not c.is_valid:
                return c.error_message
        return None

    def validate(self) -> bool:
        return all([c.validate() for c in [self.meeting_date, self.meeting_time]])

    def clear_validation_state(self):
        return self.parent().clear_validation_state()


class NewMemberFrame(ValidationMixin, QFrame):
    # signal emitted when a team member is added, edited, or removed
    # it should refresh the members list in MeetingMemberGroup
    team_member_changed = Signal()

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.id = None

        self.member_data = QFrame(self)
        self.member_data.setFixedHeight(0)
        member_data_layout = QHBoxLayout(self.member_data)
        member_data_layout.setContentsMargins(0, 0, 0, 0)
        self.member_name = LabeledInputComponent("Imię i nazwisko", self.member_data)
        self.member_function = LabeledInputComponent("Funkcja", self.member_data)
        member_data_layout.addWidget(self.member_name)
        member_data_layout.addWidget(self.member_function)

        new_member_buttons = QFrame(self)
        new_member_buttons_layout = QHBoxLayout(new_member_buttons)
        new_member_buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.show_new_member_inputs_btn = QPushButton("Dodaj", new_member_buttons)
        self.show_new_member_inputs_btn.clicked.connect(self.show_member_data_inputs)
        self.save_new_member_btn = QPushButton("Zapisz", new_member_buttons)
        self.save_new_member_btn.setVisible(False)
        self.save_new_member_btn.clicked.connect(self.save_new_member_data)
        self.edit_member_btn = QPushButton("Edytuj", new_member_buttons, enabled=False)
        self.edit_member_btn.clicked.connect(self.edit_member)
        self.remove_member_btn = QPushButton("Usuń", new_member_buttons, enabled=False)
        self.remove_member_btn.clicked.connect(self.remove_member)
        self.cancel_btn = QPushButton("Anuluj", new_member_buttons)
        self.cancel_btn.clicked.connect(self.clear)
        self.cancel_btn.setVisible(False)

        new_member_buttons_layout.addWidget(self.show_new_member_inputs_btn)
        new_member_buttons_layout.addWidget(self.save_new_member_btn)
        new_member_buttons_layout.addWidget(self.edit_member_btn)
        new_member_buttons_layout.addWidget(self.remove_member_btn)
        new_member_buttons_layout.addWidget(self.cancel_btn)

        layout.addWidget(self.member_data)
        layout.addWidget(new_member_buttons)

    def clear(self) -> None:
        self.id = None
        self.member_name.clear()
        self.member_function.clear()
        self.show_new_member_inputs_btn.setVisible(True)
        self.save_new_member_btn.setVisible(False)
        self.edit_member_btn.setVisible(True)
        self.remove_member_btn.setVisible(True)
        self.cancel_btn.setVisible(False)
        self.member_data.setFixedHeight(0)

    def show_member_data_inputs(self) -> None:
        self.member_data.setFixedHeight(45)
        self.show_new_member_inputs_btn.setVisible(False)
        self.edit_member_btn.setVisible(False)
        self.remove_member_btn.setVisible(False)
        self.save_new_member_btn.setVisible(True)
        self.cancel_btn.setVisible(True)

    def save_new_member_data(self) -> None:
        if self.id:
            member_data = TeamMemberDbSchema(id=self.id, name=self.member_name.text, function=self.member_function.text)
            update_team_member(member_data)
        else:
            member_data = TeamMemberDbCreateSchema(name=self.member_name.text, function=self.member_function.text)
            # check if given team member already exists - next iteration when we have toasts
            insert_team_member(member_data)

        self.team_member_changed.emit()
        self.clear()

    def edit_member(self) -> None:
        self.show_member_data_inputs()
        selected_members_id = self.parent().selected_members_id
        if not selected_members_id:
            return
        self.id = selected_members_id[0]
        member_data = get_meeting_member_by_id(self.id)
        self.member_name.text = member_data.name
        self.member_function.text = member_data.function
        member_data = TeamMemberDbSchema(
            id=self.id,
            name=self.member_name.text,
            function=self.member_function.text,
        )

    def remove_member(self) -> None:
        selected_members_id = self.parent().selected_members_id
        if not selected_members_id:
            return
        delete_team_member(selected_members_id[0])
        self.team_member_changed.emit()


class MeetingMemberGroup(ValidationMixin, QGroupBox):
    # signal emitted when the selection changes
    # it should result in updating the meeting leader combobox
    selection_changed = Signal()

    def __init__(self, title: str, parent: QWidget):
        super().__init__(title=title, parent=parent)
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        self.model = QStandardItemModel()
        self.model.itemChanged.connect(self.item_changed)
        self.listView = QListView(self)
        self.listView.setModel(self.model)

        self.new_member_frame = NewMemberFrame(self)
        self.new_member_frame.team_member_changed.connect(self.populate_meeting_members)

        layout.addWidget(self.listView)
        layout.addWidget(self.new_member_frame)

    @property
    def selected_members_id(self) -> list[int]:
        return [
            item.data()
            for item in self.model.findItems("*", Qt.MatchWildcard)
            if item.checkState() == Qt.CheckState.Checked
        ]

    def populate_meeting_members(self, meeting_members: list[MeetingMemberData] | None = None) -> None:
        selected_members_id = self.selected_members_id
        self.model.clear()
        meeting_members = self.get_meeting_members()

        for meeting_member_data in meeting_members:
            item = QStandardItem(f"{meeting_member_data['name']} - {meeting_member_data['function']}")
            item.setData(meeting_member_data["id"])
            item.setCheckable(True)
            item.setCheckState(
                Qt.CheckState.Checked if meeting_member_data["id"] in selected_members_id else Qt.CheckState.Unchecked
            )
            self.model.appendRow(item)

        self.selection_changed.emit()

    def clear_selection(self) -> None:
        for row_index in range(0, self.model.rowCount()):
            member = self.model.item(row_index)
            member.setCheckState(Qt.CheckState.Unchecked)

    def item_changed(self):
        self.new_member_frame.edit_member_btn.setEnabled(len(self.selected_members_id) == 1)
        self.new_member_frame.remove_member_btn.setEnabled(len(self.selected_members_id) == 1)
        self.selection_changed.emit()
        self.clear_validation_state()

    def get_meeting_members(self) -> dict:
        return [tm.model_dump() for tm in get_team_members()]

    def clear(self) -> None:
        self.new_member_frame.clear()
        self.populate_meeting_members()
        self.clear_selection()

    @property
    def is_valid(self) -> bool:
        return len(self.selected_members_id) > 1

    @property
    def error_message(self) -> str | None:
        if len(self.selected_members_id) < 2:
            return "Należy wybrać co najmniej dwóch członków zespołu."
        return None

    def display_validation_result(self, validation_result: bool):
        if validation_result:
            self.listView.setStyleSheet("background-color: lightgreen;")
        else:
            self.listView.setStyleSheet("background-color: mistyrose;")

    def validate(self) -> bool:
        self.display_validation_result(self.is_valid)
        return self.is_valid

    def clear_validation_state(self):
        self.listView.setStyleSheet("")
        return self.parent().clear_validation_state()


class MeetingTabContainer(ValidationMixin, QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.application_container = parent
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)

        self.meeting_datetime_frame = MeetingDatetimeFrame(self)
        self.meeting_date = self.meeting_datetime_frame.meeting_date
        self.meeting_time = self.meeting_datetime_frame.meeting_time

        self.meeting_member_group = MeetingMemberGroup("Członkowie zespołu", self)
        self.meeting_member_group.selection_changed.connect(self.meeting_member_selection_changed)

        self.meeting_leader = LabeledComboBoxComponent("Przewodniczący zespołu", self, required=True)
        self.meeting_leader.combobox.setPlaceholderText("Wybierz z listy...")

        layout.addWidget(self.meeting_datetime_frame)
        layout.addWidget(self.meeting_member_group)
        layout.addWidget(self.meeting_leader)
        self.meeting_member_group.populate_meeting_members()

    def meeting_member_selection_changed(self) -> None:
        self.meeting_leader.combobox.clear()
        for row_index in range(0, self.meeting_member_group.model.rowCount()):
            member = self.meeting_member_group.model.item(row_index)
            if member.checkState() == Qt.CheckState.Unchecked:
                continue
            self.meeting_leader.combobox.addItem(member.text(), member.data())

    def get_meeting_members_data(self) -> dict:
        return [tm.model_dump() for tm in get_team_members()]

    @property
    def meeting_data(self) -> MeetingData:
        meeting_members = list()
        for row_index in range(0, self.meeting_member_group.model.rowCount()):
            member = self.meeting_member_group.model.item(row_index)
            if member.checkState() == Qt.CheckState.Unchecked:
                continue
            meeting_member_data = get_meeting_member_by_id(member.data())
            if meeting_member_data.name == self.meeting_leader.combobox.currentText():
                meeting_members.insert(0, meeting_member_data)
            else:
                meeting_members.append(meeting_member_data)

        return MeetingData(
            members=meeting_members, date=self.meeting_date.date_input.date().toPython(), time=self.meeting_time.text
        )

    def clear(self):
        self.meeting_leader.remove_selection()
        self.meeting_date.date_input.setDate(QDate.currentDate())
        self.meeting_time.clear()
        self.meeting_member_group.clear()

    def populate_data(self, document_data: DocumentData) -> None:
        self.clear()
        meeting_data = document_data.meeting_data
        self.meeting_date.date_input.setDate(meeting_data.date)
        self.meeting_time.text = meeting_data.time
        self.meeting_member_group.populate_meeting_members(meeting_data.members)
        self.meeting_leader.combobox.setCurrentText(meeting_data.members[0].name)

    @property
    def is_valid(self) -> bool:
        return all(c.is_valid for c in [self.meeting_datetime_frame, self.meeting_member_group])

    @property
    def error_message(self) -> str | None:
        for c in [self.meeting_datetime_frame, self.meeting_member_group]:
            if not c.is_valid:
                return c.error_message
        return None

    def validate(self) -> bool:
        results = [c.validate() for c in [self.meeting_datetime_frame, self.meeting_member_group, self.meeting_leader]]
        return all(results)

    def clear_validation_state(self):
        self.application_container.clear_validation_state()
