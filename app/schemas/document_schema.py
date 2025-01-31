from datetime import date

from constants import ActivityForm, Issue, Reason
from pydantic import BaseModel, Field, model_validator


class AddressData(BaseModel):
    address: str
    town: str
    postal_code: str
    post: str | None = None
    full_address: str | None = None

    @model_validator(mode="after")
    def calculate_post(self):
        self.post = f"{self.postal_code} {self.town}"
        return self

    @model_validator(mode="after")
    def calculate_full_address(self):
        self.full_address = f"{self.address}, {self.post}"
        return self


class PersonalData(AddressData):
    full_name: str
    full_name_gen: str


class ChildData(PersonalData):
    pesel: str
    birth_place: str
    klass: str | None = Field(None, examples=["3b", "IVa"])
    student: bool
    birth_date: date | None = None
    profession: str | None = None
    student_description_genetive: str | None = Field(None, examples=["ucznia", "dziecka"])

    @model_validator(mode="after")
    def calculate_student_description_genetive(self) -> "ChildData":
        self.student_description_genetive = "ucznia" if self.student else "dziecka"
        return self

    @model_validator(mode="after")
    def calculate_date_of_birth(self) -> "ChildData":
        if self.birth_date:
            return self
        pesel = self.pesel
        year_part, month_part, day = int(pesel[0:2]), int(pesel[2:4]), int(pesel[4:6])
        year = 2000 + year_part if month_part > 20 else 1900 + year_part
        month = month_part - 20 if month_part > 20 else month_part
        self.birth_date = date(year, month, day)
        return self


class SchoolData(AddressData):
    rspo_id: int | None = None
    rspo_type_id: int | None = None
    parent_organisation_name: str | None = Field(None, examples=["Zespół Szkół Budowlanych"])
    type: str = Field(..., examples=["przedszkole", "szkoła podstawowa"])
    name: str
    description: str | None = None


class MeetingMemberData(BaseModel):
    name: str = Field(..., examples=["Krystyna Czarnecka"])
    function: str = Field(..., examples=["psycholog", "logopeda"])


class MeetingData(BaseModel):
    members: list[MeetingMemberData]
    date: date
    time: str


class SupportCenterData(AddressData):
    district_id: int | None = None
    province_id: int | None = None
    rspo: int | None = None
    name_nominative: str = Field(..., examples=["Poradnia Psychologiczno - Pedagogiczna w Poznaniu"])
    name_genetive: str = Field(..., examples=["Poradni Psychologiczno - Pedagogicznej w Poznaniu"])
    institute_name: str = Field(
        ..., examples=["Zespół Orzekający przy Poradni Psychologiczno-Pedagogicznej w Poznaniu"]
    )
    kurator: str


class DocumentData(BaseModel):
    # raw
    id: int | None = None
    child: ChildData
    school: SchoolData
    applicants: list[PersonalData]
    address_child_checkbox: bool = False
    address_first_parent_checkbox: bool = False
    issue: Issue
    period: str
    reasons: list[Reason] = Field(None, description="Can be one or more reasons")
    activity_form: ActivityForm | None = None
    decision_no: str
    application_date: date
    meeting_data: MeetingData
    support_center: SupportCenterData
    # calculated
    reason: Reason | None = Field(None, examples=[Reason.AUTYZM])
    multiple_disability_nominative: str | None = None
    multiple_disability_genetive: str | None = None
    multiple_disability_accusative: str | None = None
    issue_short: str | None = Field(None, examples=["ind_rocz"])
    reason_description_nominative_long: str | None = Field(None, examples=["niepełnosprawność sprzężona"])
    reason_description_genetive_long: str | None = Field(None, examples=["ie niepełnosprawności sprzężonej"])
    reason_description_accusative_long: str | None = Field(None, examples=["ie niepełnosprawność sprzężoną"])
    on_request: str | None = None
    parent_descriptions: str | None = None
    parents_names: str | None = None
    school_description: str | None = None
    file_no: str | None = None

    @model_validator(mode="after")
    def check_activity_form_required(self) -> "DocumentData":
        if self.issue == Issue.REWALIDACYJNE and not self.activity_form:
            raise ValueError(
                "If issue is of type 'rewalidacyjno-wychowawcze' activity form (eg 'grupowe') have to be selected."
            )
        return self

    @model_validator(mode="after")
    def check_multiple_disability(self) -> "DocumentData":
        """Check excluded together disabilities was selected"""
        if Reason.UNIEMOZLIWIAJACY in self.reasons and Reason.ZNACZNIE_UTRUDNIAJACY in self.reasons:
            raise ValueError(f"Reasons: {', '.join(self.reasons)} can't be issued together.")
        if intelecual_reasons := [reason for reason in self.reasons if reason in Reason.intelectual_reasons()]:
            if len(intelecual_reasons) > 1:
                raise ValueError(f"Two intelecutal reasons: {', '.join(intelecual_reasons)} can't be issued together.")
        if Reason.GLEBOKIE in self.reasons and len(self.reasons) > 1:
            raise ValueError("Profound intelectual disability can't be coupled.")
        if (
            any([reason for reason in self.reasons if reason in Reason.social_maladjustment_reasons()])
            and len(self.reasons) > 1
        ):
            raise ValueError("Social maladjustment reasons can't be coupled with any other reason.")
        return self

    @model_validator(mode="after")
    def calculate_reason(self) -> "DocumentData":
        self.reason = Reason.SPRZEZONA if len(self.reasons) > 1 else self.reasons[0]
        return self

    @model_validator(mode="after")
    def calculate_multiple_disability(self) -> "DocumentData":
        """
        Join two disability description and assign it do model attribute
        ie.
        self.multiple_disability_nominative = "niepełnosprawność intelektualna w stopniu lekkim, słabosłyszenie"
        """
        if self.reason == Reason.SPRZEZONA:
            for key, source in [
                ("multiple_disability_nominative", "reason_description_nominative_long"),
                ("multiple_disability_genetive", "reason_description_genetive_long"),
                ("multiple_disability_accusative", "reason_description_accusative_long"),
            ]:
                setattr(self, key, ", ".join([getattr(reason, source) for reason in self.reasons]))
        return self

    @model_validator(mode="after")
    def calculate_reason_description_long(self) -> "DocumentData":
        self.reason_description_nominative_long = self.reason.reason_description_nominative_long
        self.reason_description_genetive_long = self.reason.reason_description_genetive_long
        self.reason_description_accusative_long = self.reason.reason_description_accusative_long
        if self.reason == Reason.SPRZEZONA:
            self.reason_description_nominative_long += f": {self.multiple_disability_nominative}"
            self.reason_description_genetive_long += f": {self.multiple_disability_genetive}"
            self.reason_description_accusative_long += f": {self.multiple_disability_accusative}"
        return self

    @model_validator(mode="after")
    def calculate_on_request(self) -> "DocumentData":
        self.on_request = " i ".join([applicant.full_name for applicant in self.applicants])
        return self

    @model_validator(mode="after")
    def calculate_parent_description(self) -> "DocumentData":
        if self.address_child_checkbox or self.address_first_parent_checkbox:
            parents_names = " i ".join([parent.full_name for parent in self.applicants])
            if self.address_child_checkbox:
                parents_description = f"{parents_names}, {self.child.full_address}"
            else:
                parents_description = f"{parents_names}, {self.applicants[0].full_address}"
        else:
            parents_description = ", ".join(
                [f"{parent.full_name}, {parent.full_address}" for parent in self.applicants]
            )
        self.parent_descriptions = parents_description
        return self

    @model_validator(mode="after")
    def calculate_school_description(self) -> "DocumentData":
        self.school.description = ", ".join(
            [
                value
                for value in [
                    self.school.name,
                    self.school.full_address,
                    self.child.klass,
                    self.child.profession,
                ]
                if value
            ]
        )
        return self

    @model_validator(mode="after")
    def calculate_issue_short(self) -> "DocumentData":
        self.issue_short = "ind_rocz" if self.issue == Issue.INDYWIDUALNE_ROCZNE else self.issue.value[:4]
        return self

    @model_validator(mode="after")
    def calculate_parents_names(self) -> "DocumentData":
        self.parents_names = ", ".join([parent.full_name for parent in self.applicants])
        return self
