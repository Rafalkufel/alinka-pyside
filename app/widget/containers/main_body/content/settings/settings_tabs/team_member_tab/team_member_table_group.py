from PySide2.QtCore import QAbstractTableModel, Qt
from PySide2.QtWidgets import (
    QAbstractItemView,
    QGroupBox,
    QHeaderView,
    QTableView,
    QVBoxLayout,
    QWidget,
)
from schemas.db_schema import TeamMemberDbSchema

from app.db.queries import get_team_members, upsert_team_members


class TeamMemberTable(QAbstractTableModel):
    def __init__(self):
        super().__init__()
        self.horizontal_headers = ["id", "imię i nazwisko", "specjalność"]
        self._data = [[tm.id, tm.name, tm.function] for tm in get_team_members()]

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]

    def setData(self, index, value, *args):
        self._data[index.row()][index.column()] = value
        self.dataChanged.emit(index, index, [Qt.DisplayRole])
        return True

    def is_last_row_valid(self) -> bool:
        last_team_member = self._data[-1]
        return last_team_member[1] and last_team_member[2]

    def append_new_team_member(self):
        last_team_member = self._data[-1]
        if self.is_last_row_valid():
            new_team_member = [last_team_member[0] + 1, "", ""]
            self._data.append(new_team_member)
            self.layoutChanged.emit()

    def remove_team_member(self, row: int):
        self._data.pop(row)
        self.layoutChanged.emit()

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._data[0])

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.horizontal_headers[section]

    def flags(self, index):
        return Qt.ItemIsEditable | Qt.ItemIsSelectable | Qt.ItemIsEnabled

    def save_team_member_list(self):
        data = [TeamMemberDbSchema(id=tm[0], name=tm[1], function=tm[2]) for tm in self._data]
        upsert_team_members(data)


class TeamMemberTableGroup(QGroupBox):
    def __init__(self, parent: QWidget):
        super().__init__(title="Członkowie zespołu orzekającego", parent=parent)
        self.team_member_tab_container = parent
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)

        self.table_model = TeamMemberTable()
        self.table = QTableView()

        self.table.clicked.connect(self.row_selected_event)

        self.table.setModel(self.table_model)
        self.table.hideColumn(0)
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        layout.addWidget(self.table)

    @property
    def selected_row(self) -> int | None:
        selected_items = self.table.selectedIndexes()
        if selected_items:
            return selected_items[0].row()

        return None

    @property
    def selected_row_id(self) -> int | None:
        if self.selected_row:
            self.table_model._data[self.selected_row][0]
        return None

    def row_selected_event(self, item, **kwargs):
        footer_container = (
            self.team_member_tab_container.settings_container.content_container.main_body_container.footer_container
        )
        footer_container.settings_footer_container.footer_team_members_container.remove_selected_member_btn.setEnabled(
            True
        )
