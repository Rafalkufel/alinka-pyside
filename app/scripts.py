from db.connection import db_session
from db.models import School
from sqlalchemy import insert
from tests.fixtures import schools

GREEN = "\033[32m"


def populate_schools():
    with db_session() as db:
        print(f"{GREEN}Dodaję szkoły do bazy danych.")
        db.execute(insert(School), schools)
        db.commit()
        print(f"{GREEN}Szkoły zostały dodane.")


populate_schools()
