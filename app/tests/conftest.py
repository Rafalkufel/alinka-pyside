import copy

import pytest
from tests.fixtures import common_data


@pytest.fixture
def common_data_fixture():
    return copy.deepcopy(common_data)
