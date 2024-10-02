from PySide2.QtWidgets import QFrame, QHBoxLayout, QPushButton, QWidget

from app.db.queries import upsert_support_center
from app.schemas import SupportCenterData, SupportCenterDbSchema


class SettingsFooterContainer(QFrame):
    def __init__(self, parent: QWidget, visible: bool = False):
        super().__init__(parent)
        self.parent = parent
        layout = QHBoxLayout(self)
        layout.setContentsMargins(9, 9, 9, 9)
        self.save_btn = QPushButton("Zapisz", self)
        self.save_btn.clicked.connect(self.save_support_center_data)
        layout.addWidget(self.save_btn)

        if not visible:
            self.setVisible(visible)

    @property
    def support_center_data(self) -> SupportCenterData:
        return self.parent.parent.content_container.settings_container.support_center_data

    def save_support_center_data(self) -> None:
        support_center_data = SupportCenterDbSchema(**self.support_center_data.model_dump())
        upsert_support_center(support_center_data.model_dump())
