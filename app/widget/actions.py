from db.queries import create_decision_in_db, update_decision_in_db
from docx import generate_documents
from schemas import DecisionDbSchema


def generate_and_save_decision(decision_data: DecisionDbSchema, generate: bool = False) -> None:
    if decision_data.id:
        decision = update_decision_in_db(decision_data.dict())
    else:
        decision = create_decision_in_db(decision_data.dict())

    if generate:
        generate_documents(decision.id)
