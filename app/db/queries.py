from db.connection import db_session
from db.models import Decision, School, SupportCenter, TeamMember
from schemas import (
    DecisionDbSchema,
    SchoolDbSchema,
    SupportCenterDbSchema,
    TeamMemberDbSchema,
)
from sqlalchemy.dialects.sqlite import insert


def get_decisions_list_from_db() -> list[DecisionDbSchema]:
    with db_session() as db:
        decisions = db.query(Decision).all()
        return [DecisionDbSchema.model_validate(decision) for decision in decisions]


def get_decision_data_from_db(decision_id: int) -> DecisionDbSchema:
    with db_session() as db:
        decision = db.query(Decision).filter(Decision.id == decision_id).one()
        return DecisionDbSchema.model_validate(decision)


def create_decision_in_db(decision_data: dict) -> DecisionDbSchema:
    with db_session() as db:
        decision = Decision(**decision_data)
        db.add(decision)
        db.commit()
        return DecisionDbSchema.model_validate(decision)


def update_decision_in_db(decision_id: int, decision_data: dict) -> DecisionDbSchema:
    with db_session() as db:
        decision_id = (
            db.query(Decision).filter(Decision.id == decision_id).update(decision_data, synchronize_session="auto")
        )
        decision = db.query(Decision).filter(Decision.id == decision_id).one()
        return DecisionDbSchema.model_validate(decision)


def filter_schools_by_type(school_type: str | None = None) -> list[SchoolDbSchema]:
    with db_session() as db:
        query = db.query(School)
        if school_type:
            query = query.filter(School.type == school_type)

        return [SchoolDbSchema.model_validate(school) for school in query]


def get_school_by_name(school_name: str) -> SchoolDbSchema:
    with db_session() as db:
        school = db.query(School).filter(School.school_name == school_name).one_or_none()
        return SchoolDbSchema.model_validate(school)


def get_schools() -> list[SchoolDbSchema]:
    with db_session() as db:
        schools = db.query(School).all()
        return [SchoolDbSchema.model_validate(s) for s in schools]


def upsert_support_center(support_center_data: dict) -> SupportCenterDbSchema:
    with db_session() as db:
        if db.query(SupportCenter).where(SupportCenter.id == 1).one_or_none():
            db.query(SupportCenter).where(SupportCenter.id == 1).update(support_center_data, synchronize_session="auto")
            db.commit()
            support_center = db.query(SupportCenter).where(SupportCenter.id == 1).one()
        else:
            support_center = SupportCenter(**support_center_data)
            db.add(support_center)
            db.commit()

        return SupportCenterDbSchema.model_validate(support_center)


def get_support_center_data() -> SupportCenterDbSchema | None:
    with db_session() as db:
        support_center = db.query(SupportCenter).where(SupportCenter.id == 1).one_or_none()
        if support_center:
            return SupportCenterDbSchema.model_validate(support_center)


def create_school(school_data: dict) -> SchoolDbSchema:
    with db_session() as db:
        school = School(**school_data)
        db.add(school)
        db.commit()
        return SchoolDbSchema.model_validate(school)


def get_team_members() -> list[TeamMemberDbSchema]:
    with db_session() as db:
        team_members = db.query(TeamMember).all()
        return [TeamMemberDbSchema.model_validate(tm) for tm in team_members]


def upsert_team_members(team_members_data: list[TeamMemberDbSchema]) -> list[TeamMemberDbSchema]:
    with db_session() as db:
        for tm in team_members_data:
            upsert_stmt = (
                insert(TeamMember)
                .values(tm.model_dump())
                .on_conflict_do_update(index_elements=["id"], set_={"name": tm.name, "function": tm.function})
            )
            db.execute(upsert_stmt)
        db.commit()
    return get_team_members()
