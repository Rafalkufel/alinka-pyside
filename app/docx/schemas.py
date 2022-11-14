from datetime import date, time

from docx.constants import Issues, Reasons
from pydantic import BaseModel, root_validator


class AddressData(BaseModel):
    address: str
    city: str
    postal_code: str
    post: str | None
    full_address: str | None

    @root_validator(pre=True)
    def calculate_post(cls, values):
        values["post"] = f"{values['postal_code']} {values['city']}"
        return values

    @root_validator
    def calculate_full_address(cls, values):
        address, post = values["address"], values["post"]
        values["full_address"] = f"{address}, {post}"
        return values


class PersonalData(AddressData):
    first_name: str
    last_name: str
    full_name: str | None

    @root_validator
    def calculate_full_name(cls, values):
        values["full_name"] = f"{values['first_name']} {values['last_name']}"

        return values


class ChildData(PersonalData):
    pesel: str
    birth_date: date
    birth_place: str
    klass: str | None
    profession: str | None


class SchoolData(AddressData):
    school_type: str
    school_name: str
    post: str
    school_description: str | None


class MeetingMemberData(BaseModel):
    name: str
    function: str


class MeetingData(BaseModel):
    date: date
    hour: time
    members: list[MeetingMemberData]


class SupportCenterData(AddressData):
    name_nominative: str
    name_genetive: str
    institute_name: str
    kurator: str


class DocumentData(BaseModel):
    child: ChildData
    address_child_checkbox: bool = False
    address_first_parent_checkbox: bool = False
    issue: Issues
    issue_short: str | None
    period: str
    reason: Reasons
    second_reason: Reasons | None
    reason_genetive: str | None
    application_description_genetive: str | None
    multiple_disability: list[str] = []
    no: str
    school: SchoolData
    school_description: str | None
    applicants: list[PersonalData]
    meeting_data: MeetingData
    support_center: SupportCenterData
    on_request: str | None
    parent_descriptions: str | None
    parents_names: str | None

    class Config:
        use_enum_values = True

    @root_validator
    def calculate_on_request(cls, values):
        values["on_request"] = " i ".join([applicant.full_name for applicant in values["applicants"]])
        return values

    @root_validator
    def calculate_parent_description(cls, values):
        applicants = values["applicants"]
        address_first_parent_checkbox = values["address_first_parent_checkbox"]
        address_child_checkbox = values["address_child_checkbox"]
        if address_child_checkbox or address_first_parent_checkbox:
            parents_names = " i ".join([parent.full_name for parent in applicants])
            if address_child_checkbox:
                parents_description = f"{parents_names}, {values['child'].full_address}"
            else:
                parents_description = f"{parents_names}, {applicants[0].full_address}"
        else:
            parents_description = ", ".join([f"{parent.full_name}, {parent.full_address}" for parent in applicants])
        values["parent_descriptions"] = parents_description
        return values

    @root_validator
    def calculate_school_description(cls, values):
        school, child = values["school"], values["child"]
        school.school_description = ", ".join(
            [value for value in [school.school_name, school.full_address, child.klass, child.profession] if value]
        )
        return values

    @root_validator
    def calculate_issue_short(cls, values):
        issue = values["issue"]
        if issue == Issues.INDYWIDUALNE_ROCZNE:
            values["issue_short"] = "ind_rocz"
        else:
            values["issue_short"] = issue[:4]
        return values

    @root_validator
    def calculate_multiple_disability(cls, values):
        reason, second_reason = values["reason"], values["second_reason"]
        if reason and second_reason:
            values["multiple_disability"] = [reason, second_reason]
            values["reason"] = Reasons.SPRZEZONA
        return values

    @root_validator
    def calculate_parents_names(cls, values):
        applicants = values["applicants"]
        values["parents_names"] = ", ".join([parent.full_name for parent in applicants])
        return values
