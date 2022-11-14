import pytest
from docx.schemas import AddressData, DocumentData
from tests.fixtures import applicants_data, child_data, school_data, support_center_data


class TestAddressData:
    @pytest.mark.parametrize(
        "entity_with_address", [child_data, support_center_data, applicants_data[0], applicants_data[1], school_data]
    )
    def test_address_data_full_address(self, entity_with_address):
        address_data = entity_with_address.copy()
        expected_address = f"{address_data['address']}, {address_data['postal_code']} {address_data['city']}"

        address = AddressData(**address_data)

        assert address.full_address == expected_address

    @pytest.mark.parametrize(
        "entity_with_address", [child_data, support_center_data, applicants_data[0], applicants_data[1], school_data]
    )
    def test_address_data_post(self, entity_with_address):
        address_data = entity_with_address.copy()
        expected_address = f"{address_data['postal_code']} {address_data['city']}"

        address = AddressData(**address_data)

        assert address.post == expected_address


class TestParentDescription:
    @pytest.mark.parametrize("address_first_parent_checkbox", [True])
    def test_parent_description_one_parent_different_flats(self, address_first_parent_checkbox, common_data_fixture):
        del common_data_fixture["applicants"][-1]
        applicants = common_data_fixture["applicants"]
        expected_description = (
            f"{applicants[0]['first_name']} {applicants[0]['last_name']},"
            f" {applicants[0]['address']}, {applicants[0]['postal_code']} {applicants[0]['city']}"
        )
        common_data_fixture["address_child_checkbox"] = False
        common_data_fixture["address_first_parent_checkbox"] = address_first_parent_checkbox

        document_data = DocumentData(**common_data_fixture)

        assert document_data.parent_descriptions == expected_description

    @pytest.mark.parametrize("address_first_parent_checkbox", [True, False])
    def test_parent_description_one_parent_same_flat(self, address_first_parent_checkbox, common_data_fixture):
        del common_data_fixture["applicants"][-1]
        applicants = common_data_fixture["applicants"]
        child = common_data_fixture["child"]
        expected_description = (
            f"{applicants[0]['first_name']} {applicants[0]['last_name']},"
            f" {child['address']}, {child['postal_code']} {child['city']}"
        )
        common_data_fixture["address_child_checkbox"] = True
        common_data_fixture["address_first_parent_checkbox"] = address_first_parent_checkbox

        document_data = DocumentData(**common_data_fixture)

        assert document_data.parent_descriptions == expected_description

    @pytest.mark.parametrize("address_first_parent_checkbox", [True, False])
    def test_parent_description_two_parents_same_flat_as_child(
        self, address_first_parent_checkbox, common_data_fixture
    ):
        applicants = common_data_fixture["applicants"]
        child = common_data_fixture["child"]
        expected_description = (
            f"{applicants[0]['first_name']} {applicants[0]['last_name']} i"
            f" {applicants[1]['first_name']} {applicants[1]['last_name']},"
            f" {child['address']}, {child['postal_code']} {child['city']}"
        )
        common_data_fixture["address_child_checkbox"] = True
        common_data_fixture["address_first_parent_checkbox"] = address_first_parent_checkbox

        document_data = DocumentData(**common_data_fixture)

        assert document_data.parent_descriptions == expected_description

    def test_parent_description_two_parents_diffrent_flat_as_child(self, common_data_fixture):
        applicants = common_data_fixture["applicants"]
        expected_description = (
            f"{applicants[0]['first_name']} {applicants[0]['last_name']} i"
            f" {applicants[1]['first_name']} {applicants[1]['last_name']},"
            f" {applicants[0]['address']}, {applicants[0]['postal_code']} {applicants[0]['city']}"
        )
        common_data_fixture["address_child_checkbox"] = False
        common_data_fixture["address_first_parent_checkbox"] = True

        document_data = DocumentData(**common_data_fixture)

        assert document_data.parent_descriptions == expected_description

    def test_parent_description_two_parents_each_different_flat(self, common_data_fixture):
        applicants = common_data_fixture["applicants"]
        expected_description = (
            f"{applicants[0]['first_name']} {applicants[0]['last_name']},"
            f" {applicants[0]['address']}, {applicants[0]['postal_code']} {applicants[0]['city']},"
            f" {applicants[1]['first_name']} {applicants[1]['last_name']},"
            f" {applicants[1]['address']}, {applicants[1]['postal_code']} {applicants[1]['city']}"
        )
        common_data_fixture["address_child_checkbox"] = False
        common_data_fixture["address_first_parent_checkbox"] = False

        document_data = DocumentData(**common_data_fixture)

        assert document_data.parent_descriptions == expected_description
