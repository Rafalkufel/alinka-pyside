from schemas import (
    ChildData,
    DecisionDbSchema,
    DocumentData,
    MeetingData,
    MeetingMemberData,
    PersonalData,
    SchoolData,
    SupportCenterData,
)


def get_applicants_data(raw_documents_data: DecisionDbSchema) -> list[PersonalData]:
    applicants = [
        PersonalData(
            first_name=raw_documents_data.first_parent_first_name,
            last_name=raw_documents_data.first_parent_last_name,
            address=raw_documents_data.first_parent_address,
            city=raw_documents_data.first_parent_city,
            postal_code=raw_documents_data.first_parent_postal_code,
        )
    ]
    first_name, last_name = raw_documents_data.second_parent_first_name, raw_documents_data.second_parent_last_name
    if first_name and last_name:
        applicants.append(
            PersonalData(
                first_name=first_name,
                last_name=last_name,
                address=raw_documents_data.second_parent_address,
                city=raw_documents_data.second_parent_city,
                postal_code=raw_documents_data.second_parent_postal_code,
            )
        )
    return applicants


def get_meeting_data(raw_documents_data: DecisionDbSchema) -> MeetingData:
    return MeetingData(
        members=[MeetingMemberData(**member_data) for member_data in raw_documents_data.meeting_members],
        date=raw_documents_data.meeting_date,
        time=raw_documents_data.meeting_time,
    )


def convert_raw_documents_data(raw_documents_data: DecisionDbSchema) -> DocumentData:
    child_data = ChildData(
        address=raw_documents_data.child_address,
        city=raw_documents_data.child_city,
        postal_code=raw_documents_data.child_postal_code,
        student=raw_documents_data.child_student,
        first_name=raw_documents_data.child_first_name,
        last_name=raw_documents_data.child_last_name,
        pesel=raw_documents_data.child_pesel,
        profession=raw_documents_data.profession,
        birth_date=raw_documents_data.child_birth_date,
        birth_place=raw_documents_data.child_birth_place,
    )
    school_data = SchoolData(
        address=raw_documents_data.school_address,
        city=raw_documents_data.school_city,
        postal_code=raw_documents_data.school_postal_code,
        school_name=raw_documents_data.school_name,
        parent_organisation=raw_documents_data.school_parent_organisation,
        school_type=raw_documents_data.school_type,
    )
    meeting_data = MeetingData(
        members=[MeetingMemberData(**member_data) for member_data in raw_documents_data.meeting_members],
        date=raw_documents_data.meeting_date,
        time=raw_documents_data.meeting_time,
    )
    support_center_data = SupportCenterData(
        name_nominative=raw_documents_data.support_center_name_nominative,
        name_genetive=raw_documents_data.support_center_name_genetive,
        kurator=raw_documents_data.support_center_kurator,
        address=raw_documents_data.support_center_address,
        city=raw_documents_data.support_center_city,
        postal_code=raw_documents_data.support_center_postal_code,
        institute_name=raw_documents_data.support_center_institute_name,
    )
    return DocumentData(
        child=child_data,
        address_child_checkbox=raw_documents_data.address_child_checkbox,
        address_first_parent_checkbox=raw_documents_data.address_first_parent_checkbox,
        issue=raw_documents_data.issue,
        reasons=raw_documents_data.reasons,
        activity_form=raw_documents_data.activity_form,
        no=raw_documents_data.no,
        school=school_data,
        applicants=get_applicants_data(raw_documents_data),
        application_date=raw_documents_data.application_date,
        meeting_data=meeting_data,
        support_center=support_center_data,
        period=raw_documents_data.period,
    )
