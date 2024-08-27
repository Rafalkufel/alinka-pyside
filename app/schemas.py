from datetime import date

from constants import ActivityForm, Issue, Reason
from pydantic import BaseModel, Field, root_validator


class DecisionDbSchema(BaseModel):
    class Config:
        orm_mode = True

    id: int | None

    child_full_name: str
    child_full_name_gen: str
    child_address: str
    child_town: str
    child_postal_code: str | None
    child_post: str | None
    child_pesel: str
    child_birth_date: date
    child_birth_place: str
    child_student: bool = True
    klass: str | None
    profession: str | None

    school_parent_organisation: str | None
    school_type: str
    school_name: str
    school_address: str
    school_town: str
    school_postal_code: str
    school_post: str | None

    address_child_checkbox: bool = False
    address_first_parent_checkbox: bool = False
    first_parent_full_name: str
    first_parent_full_name_gen: str
    first_parent_address: str
    first_parent_town: str
    first_parent_postal_code: str | None
    first_parent_post: str | None
    second_parent_full_name: str | None
    second_parent_full_name_gen: str | None
    second_parent_address: str | None
    second_parent_town: str | None
    second_parent_postal_code: str | None
    second_parent_post: str | None

    support_center_name_nominative: str | None
    support_center_name_genetive: str | None
    support_center_institute_name: str | None
    support_center_kurator: str | None
    support_center_address: str | None
    support_center_town: str | None
    support_center_postal_code: str | None

    issue: str
    period: str
    reasons: list[str]
    activity_form: str | None
    decision_no: str
    application_date: date
    meeting_date: date
    meeting_time: str
    meeting_members: list[dict[str, str]]

    file_no = str


class SchoolDBSchema(BaseModel):
    class Config:
        orm_mode = True

    id: int
    school_parent_organisation: str | None
    school_type: str
    school_name: str
    school_address: str
    school_town: str
    school_postal_code: str
    school_post: str


class AddressData(BaseModel):
    address: str
    town: str
    postal_code: str
    post: str | None
    full_address: str | None

    @root_validator(pre=True)
    def calculate_post(cls, values):
        values["post"] = f"{values['postal_code']} {values['town']}"
        return values

    @root_validator
    def calculate_full_address(cls, values):
        address, post = values["address"], values["post"]
        values["full_address"] = f"{address}, {post}"
        return values


class PersonalData(AddressData):
    full_name: str
    full_name_gen: str


class ChildData(PersonalData):
    pesel: str
    birth_place: str
    klass: str | None = Field(None, description="'klass' to avoid overriding 'class' keyword", example="3b or IVa")
    student: bool
    birth_date: date | None
    profession: str | None
    student_description_genetive: str | None = Field(None, description="'ucznia' or 'dziecka'")

    @root_validator
    def calculate_student_description_genetive(cls, values):
        values["student_description_genetive"] = "ucznia" if values["student"] else "dziecka"
        return values

    @root_validator
    def calculate_date_of_birth(cls, values) -> dict:
        if values["birth_date"]:
            return values
        pesel = values["pesel"]
        year_part, month_part, day = int(pesel[0:2]), int(pesel[2:4]), int(pesel[4:6])
        year = 2000 + year_part if month_part > 20 else 1900 + year_part
        month = month_part - 20 if month_part > 20 else month_part
        values["birth_date"] = date(year, month, day)
        return values


class SchoolData(AddressData):
    parent_organisation: str | None = Field(None, description="eg. 'Zespół Szkół Budowlanych'")
    school_type: str = Field(..., description="'przedszkole', 'szkoła podstawowa'")
    school_name: str
    school_description: str | None


class MeetingMemberData(BaseModel):
    name: str = Field(..., description="Krystyna Czarnecka")
    function: str = Field(..., description="psycholog, logopeda")


class MeetingData(BaseModel):
    members: list[MeetingMemberData]
    date: date
    time: str


class SupportCenterData(AddressData):
    name_nominative: str = Field(..., description="Poradnia Psychologiczno - Pedagogiczna w Poznaniu")
    name_genetive: str = Field(..., description="Poradni Psychologiczno - Pedagogicznej w Poznaniu")
    institute_name: str = Field(
        ..., description="Zespół Orzekający przy Poradni Psychologiczno-Pedagogicznej w Poznaniu"
    )
    kurator: str


class DocumentData(BaseModel):
    # raw
    id: int | None
    child: ChildData
    school: SchoolData
    applicants: list[PersonalData]
    address_child_checkbox: bool = False
    address_first_parent_checkbox: bool = False
    issue: Issue
    period: str
    reasons: list[Reason] = Field(None, description="Can be one or more reasons")
    activity_form: ActivityForm | None
    decision_no: str
    application_date: date
    meeting_data: MeetingData
    support_center: SupportCenterData
    # calculated
    reason: Reason | None = Field(None, example="Reason.SPRZEZONA | Reason.AUTYZM")
    multiple_disability_nominative: str | None
    multiple_disability_genetive: str | None
    multiple_disability_accusative: str | None
    issue_short: str | None = Field(None, example="'spec', 'ind_rocz', 'indy'")
    reason_description_nominative_long: str | None = Field(None, example="niepełnosprawność sprzężona")
    reason_description_genetive_long: str | None = Field(None, example="niepełnosprawności sprzężonej")
    reason_description_accusative_long: str | None = Field(None, example="niepełnosprawność sprzężoną")
    on_request: str | None
    parent_descriptions: str | None
    parents_names: str | None
    school_description: str | None
    file_no: str | None

    @root_validator
    def check_activity_form_required(cls, values):
        issue, activity_form = values["issue"], values.get("activity_form")
        if issue == Issue.REWALIDACYJNE and not activity_form:
            raise ValueError(
                "If issue is of type 'rewalidacyjno-wychowawcze' activity form (eg 'grupowe') have to be selected."
            )
        return values

    @root_validator
    def check_multiple_disability(cls, values):
        """Check excluded together disabilities was selected"""
        reasons = values["reasons"]
        if Reason.UNIEMOZLIWIAJACY in reasons and Reason.ZNACZNIE_UTRUDNIAJACY in reasons:
            raise ValueError(f"Reasons: {', '.join(reasons)} can't be issued together.")
        if intelecual_reasons := [reason for reason in reasons if reason in Reason.intelectual_reasons()]:
            if len(intelecual_reasons) > 1:
                raise ValueError(f"Two intelecutal reasons: {', '.join(intelecual_reasons)} can't be issued together.")
        if Reason.GLEBOKIE in reasons and len(reasons) > 1:
            raise ValueError("Profound intelectual disability can't be coupled.")
        if any([reason for reason in reasons if reason in Reason.social_maladjustment_reasons()]) and len(reasons) > 1:
            raise ValueError("Social maladjustment reasons can't be coupled with any other reason.")
        return values

    @root_validator
    def calculate_reason(cls, values):
        values["reason"] = Reason.SPRZEZONA if len(values["reasons"]) > 1 else values["reasons"][0]
        return values

    @root_validator
    def calculate_multiple_disability(cls, values):
        reason, reasons = values["reason"], values["reasons"]
        if reason == Reason.SPRZEZONA:
            for key, source in [
                ("multiple_disability_nominative", "reason_description_nominative_long"),
                ("multiple_disability_genetive", "reason_description_genetive_long"),
                ("multiple_disability_accusative", "reason_description_accusative_long"),
            ]:
                values[key] = ", ".join([getattr(reason, source) for reason in reasons])
        return values

    @root_validator
    def calculate_reason_description_long(cls, values):
        reason = values["reason"]
        values["reason_description_nominative_long"] = reason.reason_description_nominative_long
        values["reason_description_genetive_long"] = reason.reason_description_genetive_long
        values["reason_description_accusative_long"] = reason.reason_description_accusative_long
        if reason == Reason.SPRZEZONA:
            values["reason_description_nominative_long"] += f": {values['multiple_disability_nominative']}"
            values["reason_description_genetive_long"] += f": {values['multiple_disability_genetive']}"
            values["reason_description_accusative_long"] += f": {values['multiple_disability_accusative']}"
        return values

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
        values["issue_short"] = "ind_rocz" if issue == Issue.INDYWIDUALNE_ROCZNE else issue.value[:4]
        return values

    @root_validator
    def calculate_parents_names(cls, values):
        applicants = values["applicants"]
        values["parents_names"] = ", ".join([parent.full_name for parent in applicants])
        return values
