from PySide2.QtWidgets import QFrame, QHBoxLayout, QPushButton, QVBoxLayout, QWidget


class SidebarMenuContainer(QFrame):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(9, 9, 9, 9)
        search_child_btn = QPushButton("Wyszukaj dziecko", self)
        layout.addWidget(search_child_btn)
        create_documents_btn = QPushButton("Utwórz dokument", self)
        layout.addWidget(create_documents_btn)
        settings_btn = QPushButton("Ustawienia", self)
        layout.addWidget(settings_btn)


class SidebarMenu(QFrame):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(9, 9, 9, 9)
        main_container = SidebarMenuContainer(self)
        layout.addWidget(main_container)
