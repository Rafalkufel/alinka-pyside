from PySide6.QtWidgets import QVBoxLayout, QWidget

from .school_data_group import SchoolDataGroup
from .select_school_group import SelectSchoolGroup


class SchoolTabContainer(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        self.select_schools_region_group = SelectSchoolGroup(self)
        layout.addWidget(self.select_schools_region_group)

        self.school_data_group = SchoolDataGroup(self)
        layout.addWidget(self.school_data_group)

    @property
    def is_valid(self) -> bool:
        return True

    @property
    def error_message(self) -> str | None:
        return None
