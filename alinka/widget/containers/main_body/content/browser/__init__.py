from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QHeaderView,
    QTableView,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from alinka.db.queries import filter_decisions_by_pesel_child_name
from alinka.schemas.db_schema import DecisionDbSchema
from alinka.widget.components import LabeledInputComponent


class DecisionsTableModel(QAbstractTableModel):
    filter_by: str | None

    def __init__(self, parent=None):
        super().__init__(parent)
        self.filter_by = None

    @staticmethod
    def map_model_to_row_data(decision: DecisionDbSchema) -> list[str]:
        return [
            decision.id,
            decision.child_pesel,
            decision.child_full_name,
            f"{decision.child_town}, {decision.child_address}",
        ]

    @property
    def _data(self):
        decisions = filter_decisions_by_pesel_child_name(self.filter_by)
        return [self.map_model_to_row_data(decision) for decision in decisions]

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self._data)

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self.header_names)

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]

    @property
    def header_names(self):
        return ["id", "PESEL dziecka", "Imię i nazwisko dziecka", "Adres dziecka"]

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                try:
                    return self.header_names[section]
                except Exception as exc:
                    print(exc)
                    raise
            else:
                return section + 1


class BrowseDecisionContainer(QWidget):
    selected_decision_id: int | None

    def __init__(self, parent: QWidget):
        self.browser_container = parent
        super().__init__(parent)
        self.selected_decision_id = None
        layout = QVBoxLayout(self)
        browse_input = LabeledInputComponent("Szukaj", self)
        browse_input.line_edit.textChanged.connect(self.entered_filter_by)

        self.table_model = DecisionsTableModel()
        self.decision_table = QTableView(self)
        self.decision_table.setModel(self.table_model)
        self.decision_table.setColumnHidden(0, True)
        self.decision_table.resizeColumnsToContents()
        self.decision_table.setSelectionBehavior(QAbstractItemView.SelectRows)

        header = self.decision_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Fixed)
        header.setSectionResizeMode(1, QHeaderView.Fixed)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.Stretch)

        layout.addWidget(browse_input)
        layout.addWidget(self.decision_table)

    def entered_filter_by(self, text):
        if self.table_model.filter_by != text:
            self.table_model.filter_by = text
            self.table_model.beginResetModel()
            self.table_model.endResetModel()

    def showEvent(self, event):
        # this refreshes browser whenever tab is shown:
        self.table_model.beginResetModel()
        self.table_model.endResetModel()
        return super().showEvent(event)


class BrowserContainer(QTabWidget):
    def __init__(self, parent: QWidget, visible: bool = False):
        super().__init__(parent)
        self.content_container = parent
        self.browse_decision_container = BrowseDecisionContainer(self)
        self.addTab(self.browse_decision_container, "Wyszukaj dokument")

        self.setVisible(visible)
