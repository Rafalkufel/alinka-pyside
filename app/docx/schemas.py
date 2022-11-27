from datetime import date, time

from docx.constants import ActivityForm, Issue, Reason
from pydantic import BaseModel, Field, root_validator


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
    student: bool
    profession: str | None
    student_description_genetive: str | None

    @root_validator
    def calculate_student_description_genetive(cls, values):
        values["student_description_genetive"] = "ucznia" if values["student"] else "dziecka"
        return values


class SchoolData(AddressData):
    school_type: str
    school_name: str
    post: str
    school_description: str | None


class MeetingMemberData(BaseModel):
    name: str
    function: str


class MeetingData(BaseModel):
    members: list[MeetingMemberData]
    date: date
    time: time


class SupportCenterData(AddressData):
    name_nominative: str
    name_genetive: str
    institute_name: str
    kurator: str


class DocumentData(BaseModel):
    # raw
    child: ChildData
    address_child_checkbox: bool = False
    address_first_parent_checkbox: bool = False
    issue: Issue
    period: str
    reasons: list[Reason] = Field(None, description="Can be one or moe reasons")
    activity_form: ActivityForm | None
    no: str
    school: SchoolData
    applicants: list[PersonalData]
    application_date: date
    meeting_data: MeetingData
    support_center: SupportCenterData
    # calculated
    reason: Reason | None = Field(None, example="Reason.SPRZEZONA | Reason.AUTYZM")
    multiple_disability_nominative: str | None
    multiple_disability_genetive: str | None
    multiple_disability_accusative: str | None
    issue_short: str | None = Field(None, example="'spec', 'ind_rocz', 'indy'")
    issue_type_nominative_short: str | None = Field(None, example="'orzeczenie', 'opinia'")
    issue_type_genetive_short: str | None = Field(None, example="'orzeczenia', 'opinii'")
    issue_subject_nominative: str | None = Field(None, example="kształcenie specjalne")
    issue_subject_genetive: str | None = Field(None, example="kształcenia specjalnego")
    issue_type_nominative_long: str | None = Field(None, example="orzeczenie o potrzebie kształcenia specjalnego")
    issue_type_genetive_long: str | None = Field(None, example="orzeczenia o potrzebie kształcenia specjalnego")
    reason_description_nominative_short: str | None = Field(None, example="'niepełnosprawność', 'stan zdrowia'")
    reason_description_genetive_short: str | None = Field(None, example="'niepełnospraności', 'stanu zdrowia'")
    reason_description_nominative_long: str | None = Field(None, example="niepełnosprawność sprzężona")
    reason_description_genetive_long: str | None = Field(None, example="niepełnosprawności sprzężonej")
    reason_description_accusative_long: str | None = Field(None, example="niepełnosprawność sprzężoną")
    on_request: str | None
    parent_descriptions: str | None
    parents_names: str | None
    school_description: str | None

    class Config:
        use_enum_values = True

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
        if Reason.UNIEMOZLIWIAJACY.value in reasons and Reason.ZNACZNIE_UTRUDNIAJACY.value in reasons:
            raise ValueError(f"Reasons: {', '.join(reasons)} can't be issued together.")
        if intelecual_reasons := [reason for reason in reasons if reason in Reason.intelectual_reasons()]:
            if len(intelecual_reasons) > 1:
                raise ValueError(f"Two intelecutal reasons: {', '.join(intelecual_reasons)} can't be issued together.")
        if Reason.GLEBOKIE.value in reasons and len(reasons) > 1:
            raise ValueError("Profound intelectual disability can't be cupled.")
        if any([reason for reason in reasons if reason in Reason.social_maladjustment_reasons()]) and len(reasons) > 1:
            raise ValueError("Social maladjustment reasons can be coupled with any other reason.")
        return values

    @root_validator
    def calculate_reason(cls, values):
        if len(values["reasons"]) > 1:
            values["reason"] = Reason.SPRZEZONA
        else:
            values["reason"] = values["reasons"][0]
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
                values[key] = ", ".join([getattr(Reason(reason), source) for reason in reasons])
        return values

    @root_validator
    def calculate_issue_forms(cls, values):
        issue = Issue(values["issue"])
        values["issue_type_nominative_short"] = issue.issue_type_nominative_short
        values["issue_type_genetive_short"] = issue.issue_type_genetive_short
        values["issue_subject_nominative"] = issue.issue_description_nominative
        values["issue_subject_genetive"] = issue.issue_description_genetive
        values["issue_type_nominative_long"] = issue.issue_type_nominative_long
        values["issue_type_genetive_long"] = issue.issue_type_genetive_long
        return values

    @root_validator
    def calculate_reason_description_short(cls, values):
        values["reason_description_nominative_short"] = Reason(values["reason"]).reason_description_nominative_short
        values["reason_description_genetive_short"] = Reason(values["reason"]).reason_description_genetive_short
        return values

    @root_validator
    def calculate_reason_description_long(cls, values):
        reason = Reason(values["reason"])
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
        if issue == Issue.INDYWIDUALNE_ROCZNE.value:
            values["issue_short"] = "ind_rocz"
        else:
            values["issue_short"] = issue[:4]
        return values

    @root_validator
    def calculate_parents_names(cls, values):
        applicants = values["applicants"]
        values["parents_names"] = ", ".join([parent.full_name for parent in applicants])
        return values

    @root_validator
    def calculate_reason_short_description_nominative(cls, values):
        reason = values["reason"]
        if reason:
            description = "sprzężoną niepełnosprawność"
        elif reason == Reason.AUTYZM.value:
            description = "autyzm"
        elif reason == Reason.RUCHOWA.value:
            description = "niepełnosprawność ruchową"
        elif Reason(reason) in [*Reason.intelectual_reasons(), *Reason.perception_deficites_reasons()]:
            description = "stwierdzoną niepełnosprawność"
        elif reason == Reason.NIEDOSTOSOWANIE.value:
            description = "niedostosowanie społeczne"
        elif reason == Reason.ZAGROZENIE_NIEDOSTOSOWANIEM.value:
            description = "zagrożenie niedostosowaniem społecznym"

        values["reason_short_description_nominative"] = description
        return values
