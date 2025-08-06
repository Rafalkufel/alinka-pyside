from PySide6.QtWidgets import QVBoxLayout, QWidget

from .school_data_group import SchoolDataGroup
from .school_list_group import SchoolListGroup
from .select_school_group import SelectSchoolGroup


class SchoolTabContainer(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        self.select_schools_region_group = SelectSchoolGroup(self)
        layout.addWidget(self.select_schools_region_group)

        self.school_data_group = SchoolDataGroup(self)
        layout.addWidget(self.school_data_group)

        self.school_list = SchoolListGroup(self)
        layout.addWidget(self.school_list)

    @property
    def is_valid(self) -> bool:
        selected_school = self.select_schools_region_group.schools_combobox.combobox.currentText()
        return bool(selected_school)

    @property
    def error_message(self) -> str | None:
        if not self.is_valid:
            return "Brak dodanej szkoły w ustawieniach. Dodaj szkołę, aby utworzyć nowy wniosek."
        return None
