from db.queries import (
    create_decission_in_db,
    get_decission_data_from_db,
    get_decissions_list_from_db,
    update_decision_in_db,
)
from tests.factories import DecissionFactory
from tests.fixtures import decission_data


class TestQuery:
    def setup(self):
        DecissionFactory()
        DecissionFactory()
        self.decission_data = decission_data.copy()
        self.decission_1, self.decission_2 = get_decissions_list_from_db()

    def test_get_decission_list_from_db_successful(self):
        decissions = get_decissions_list_from_db()
        assert decissions == [self.decission_1, self.decission_2]

    def test_get_decission_data_from_db(self):
        decission = get_decission_data_from_db(decision_id=self.decission_1.id)
        assert decission == self.decission_1

    def test_create_decission_id_db(self):
        del decission_data["id"], decission_data["created_at"], decission_data["modified_at"]
        decission = create_decission_in_db(decision_data=decission_data)
        assert decission.child_first_name == decission_data["child_first_name"]

    def test_update_decission_in_db(self):
        new_child_name = "new child name"
        decission = update_decision_in_db(self.decission_1.id, decision_data={"child_first_name": new_child_name})
        assert decission.child_first_name == new_child_name
