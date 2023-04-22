from PySide6.QtWidgets import QLabel, QLineEdit, QMainWindow, QPushButton
from schemas import DecissionDbSchema
from tests.fixtures import decission_data as decission_fixture
from widget.actions import generate_and_save_decision


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")
        self.setGeometry(100, 100, 600, 400)
        self.ui_components()
        self.show()

    def ui_components(self):
        self.button = QPushButton("Utwórz dokumenty", self)
        self.button.setGeometry(200, 150, 150, 40)
        self.button.clicked.connect(self.click_me)
        self.input_line = QLineEdit("Mock first name", self)
        self.input_line.setGeometry(200, 100, 150, 40)
        self.result = QLabel("Wait for result...", self)
        self.result.setGeometry(200, 200, 150, 40)

    def click_me(self):
        decission_data = DecissionDbSchema(**decission_fixture)
        decission_data.child_first_name = self.input_line.text()
        decission_data.id = None
        generate_and_save_decision(decission_data, generate=True)
        self.result.setText("SUCCESS")
