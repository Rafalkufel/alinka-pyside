from datetime import date

from constants import ActivityForm, Issue, Reason
from pydantic import BaseModel, Field, computed_field, model_validator


class AddressData(BaseModel):
    address: str
    town: str | None
    postal_code: str
    post: str

    @computed_field
    def full_address(self) -> str:
        post_description = f"{self.postal_code} {self.post}"
        address_parts = [self.address]

        if self.town and self.town != self.post:
            address_parts.append(self.town)

        address_parts.append(post_description)
        return ", ".join(address_parts)


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

    @computed_field
    def student_description_genetive(self) -> str:
        return "ucznia" if self.student else "dziecka"

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
    file_no: str | None = None

    @computed_field
    def on_request(self) -> str:
        return " i ".join([applicant.full_name for applicant in self.applicants])

    @computed_field
    def parents_names(self) -> str:
        return ", ".join([parent.full_name for parent in self.applicants])

    @computed_field
    def reason(self) -> Reason:
        return Reason.SPRZEZONA if len(self.reasons) > 1 else self.reasons[0]

    @computed_field
    def multiple_disability_nominative(self) -> str | None:
        """
        Join two disability description ie.
        "niepełnosprawność intelektualna w stopniu lekkim, słabosłyszenie"
        """
        if self.reason == Reason.SPRZEZONA:
            return ", ".join([getattr(reason, "reason_description_nominative_long") for reason in self.reasons])

    @computed_field
    def multiple_disability_genetive(self) -> str | None:
        """
        Join two disability description ie.
        "niepełnosprawności intelektualnej w stopniu lekkim, słabosłyszenia"
        """
        if self.reason == Reason.SPRZEZONA:
            return ", ".join([getattr(reason, "reason_description_genetive_long") for reason in self.reasons])

    @computed_field
    def multiple_disability_accusative(self) -> str | None:
        """
        Join two disability description ie.
        "niepełnosprawność intelektualną w stopniu lekkim, słabosłyszenie"
        """
        if self.reason == Reason.SPRZEZONA:
            return ", ".join([getattr(reason, "reason_description_accusative_long") for reason in self.reasons])

    @computed_field
    def reason_description_nominative_long(self) -> str:
        """
        ie.: "niepełnosprawność ruchowa"
        or: "niepełnosprawność sprzężona: niepełnosprawność ruchowa i słabosłyszenie
        """
        reason_description_nominative_long = self.reason.reason_description_nominative_long
        if self.reason == Reason.SPRZEZONA:
            reason_description_nominative_long += f": {self.multiple_disability_nominative}"
        return reason_description_nominative_long

    @computed_field
    def reason_description_genetive_long(self) -> str:
        """
        ie.: "niepełnosprawność ruchowej"
        or: "niepełnosprawność sprzężonej: niepełnosprawności ruchowej i słabosłyszenia
        """
        reason_description_genetive_long = self.reason.reason_description_genetive_long
        if self.reason == Reason.SPRZEZONA:
            reason_description_genetive_long += f": {self.multiple_disability_genetive}"
        return reason_description_genetive_long

    @computed_field
    def reason_description_accusative_long(self) -> str:
        """
        ie.: "niepełnosprawność ruchową"
        or: "niepełnosprawność sprzężoną: niepełnosprawność ruchową i słabosłyszenie
        """
        reason_description_accusative_long = self.reason.reason_description_accusative_long
        if self.reason == Reason.SPRZEZONA:
            reason_description_accusative_long += f": {self.multiple_disability_accusative}"
        return reason_description_accusative_long

    @computed_field
    def parent_descriptions(self) -> str:
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
        return parents_description

    @computed_field
    def school_description(self) -> str:
        return ", ".join(
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

    @computed_field
    def calculate_issue_short(self) -> str:
        return "ind_rocz" if self.issue == Issue.INDYWIDUALNE_ROCZNE else self.issue.value[:4]

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
