from datetime import date

from pydantic import BaseModel, ConfigDict


class DecisionDbSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None

    child_full_name: str
    child_full_name_gen: str
    child_address: str
    child_town: str
    child_postal_code: str | None = None
    child_post: str | None = None
    child_pesel: str
    child_birth_date: date
    child_birth_place: str
    child_student: bool = True
    klass: str | None = None
    profession: str | None = None

    school_parent_organisation: str | None = None
    school_type: str
    school_name: str
    school_address: str
    school_town: str
    school_postal_code: str
    school_post: str | None = None

    address_child_checkbox: bool = False
    address_first_parent_checkbox: bool = False
    first_parent_full_name: str
    first_parent_full_name_gen: str
    first_parent_address: str
    first_parent_town: str
    first_parent_postal_code: str | None = None
    first_parent_post: str | None = None
    second_parent_full_name: str | None = None
    second_parent_full_name_gen: str | None = None
    second_parent_address: str | None = None
    second_parent_town: str | None = None
    second_parent_postal_code: str | None = None
    second_parent_post: str | None = None

    support_center_name_nominative: str | None = None
    support_center_name_genetive: str | None = None
    support_center_institute_name: str | None = None
    support_center_kurator: str | None = None
    support_center_address: str | None = None
    support_center_town: str | None = None
    support_center_postal_code: str | None = None

    issue: str
    period: str
    reasons: list[str]
    activity_form: str | None = None
    decision_no: str
    application_date: date
    meeting_date: date
    meeting_time: str
    meeting_members: list[dict[str, str]]

    file_no: str | None = None


class SchoolDBSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    school_parent_organisation: str | None = None
    school_type: str
    school_name: str
    school_address: str
    school_town: str
    school_postal_code: str
    school_post: str
