from db.connection import db_session
from db.models import Decision
from schemas import DecisionDbSchema


def get_decisions_list_from_db() -> list[DecisionDbSchema]:
    with db_session() as db:
        decisions = db.query(Decision).all()
        return [DecisionDbSchema.from_orm(decision) for decision in decisions]


def get_decision_data_from_db(decision_id: int) -> DecisionDbSchema:
    with db_session() as db:
        decision = db.query(Decision).filter(Decision.id == decision_id).one()
        return DecisionDbSchema.from_orm(decision)


def create_decision_in_db(decision_data: dict) -> DecisionDbSchema:
    with db_session() as db:
        decision = Decision(**decision_data)
        db.add(decision)
        db.commit()
        return DecisionDbSchema.from_orm(decision)


def update_decision_in_db(decision_id: int, decision_data: dict) -> DecisionDbSchema:
    with db_session() as db:
        decision_id = (
            db.query(Decision).filter(Decision.id == decision_id).update(decision_data, synchronize_session="auto")
        )
        decision = db.query(Decision).filter(Decision.id == decision_id).one()
        return DecisionDbSchema.from_orm(decision)
