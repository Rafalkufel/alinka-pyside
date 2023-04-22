from db.connection import db_session
from db.models import Decission
from schemas import DecissionDbSchema


def get_decissions_list_from_db() -> list[DecissionDbSchema]:
    with db_session() as db:
        decissions = db.query(Decission).all()
        return [DecissionDbSchema.from_orm(decission) for decission in decissions]


def get_decission_data_from_db(decision_id: int) -> DecissionDbSchema:
    with db_session() as db:
        decision = db.query(Decission).filter(Decission.id == decision_id).one()
        return DecissionDbSchema.from_orm(decision)


def create_decission_in_db(decision_data: dict):
    with db_session() as db:
        decision = Decission(**decision_data)
        db.add(decision)
        db.commit()
        return DecissionDbSchema.from_orm(decision)


def update_decision_in_db(decision_id: int, decision_data: dict):
    with db_session() as db:
        decission_id = (
            db.query(Decission).filter(Decission.id == decision_id).update(decision_data, synchronize_session="auto")
        )
        decission = db.query(Decission).filter(Decission.id == decission_id).one()
        return DecissionDbSchema.from_orm(decission)
