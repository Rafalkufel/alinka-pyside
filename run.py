import sys

from PySide6.QtSql import QSqlDatabase
from PySide6.QtWidgets import QApplication

from alinka.config import settings
from alinka.widget.main_window import MainWindow

app = QApplication(sys.argv)

qt_db = QSqlDatabase.addDatabase("QSQLITE")
qt_db.setDatabaseName(settings.DB_PATH)

# Add handling opening issues https://github.com/CodeForPoznan/alinka-pyside/issues/34
qt_db.open()

window = MainWindow()
window.show()

app.exec()
