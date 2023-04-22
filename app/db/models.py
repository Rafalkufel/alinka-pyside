from sqlalchemy import Boolean, Column, Date, DateTime, Integer, String, Time
from sqlalchemy.dialects.sqlite import JSON
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


class Decission(Base):
    __tablename__ = "decision"

    id = Column(Integer(), primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    modified_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    child_first_name = Column(String(50), nullable=False)
    child_last_name = Column(String(50), nullable=False)
    child_address = Column(String(1024), nullable=False)
    child_city = Column(String(128), nullable=False)
    child_postal_code = Column(String(12), nullable=True)
    child_pesel = Column(String(12), nullable=False)
    child_birth_date = Column(Date, nullable=False)
    child_birth_place = Column(String(100), nullable=False)
    child_student = Column(Boolean(), nullable=False, default=True)
    klass = Column(String(30), nullable=True)
    profession = Column(String(120), nullable=True)

    school_parent_organisation = Column(String(512), nullable=True)
    school_type = Column(String(50), nullable=False)
    school_name = Column(String(1024), nullable=False)
    school_address = Column(String(1024), nullable=False)
    school_city = Column(String(128), nullable=False)
    school_postal_code = Column(String(12), nullable=False)

    address_child_checkbox = Column(Boolean, nullable=False, default=False)
    address_first_parent_checkbox = Column(Boolean, nullable=False, default=False)
    first_parent_first_name = Column(String(50), nullable=False)
    first_parent_last_name = Column(String(50), nullable=False)
    first_parent_address = Column(String(1024), nullable=False)
    first_parent_city = Column(String(128), nullable=False)
    first_parent_postal_code = Column(String(12), nullable=True)
    second_parent_first_name = Column(String(50), nullable=True)
    second_parent_last_name = Column(String(50), nullable=True)
    second_parent_address = Column(String(1024), nullable=True)
    second_parent_city = Column(String(128), nullable=True)
    second_parent_postal_code = Column(String(12), nullable=True)

    support_center_name_nominative = Column(String(1024), nullable=True)
    support_center_name_genetive = Column(String(1024), nullable=True)
    support_center_institute_name = Column(String(1024), nullable=True)
    support_center_kurator = Column(String(1024), nullable=True)
    support_center_address = Column(String(1024), nullable=True)
    support_center_city = Column(String(128), nullable=True)
    support_center_postal_code = Column(String(12), nullable=True)

    issue = Column(String(256), nullable=False)
    period = Column(String(256), nullable=False)
    reasons = Column(JSON, nullable=False)
    activity_form = Column(String(20), nullable=True)
    no = Column(String(15), nullable=False)
    application_date = Column(Date, nullable=False)
    meeting_date = Column(Date, nullable=False)
    meeting_time = Column(Time, nullable=False)
    meeting_members = Column(JSON, nullable=False)
