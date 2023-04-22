import copy
from contextlib import contextmanager
from unittest.mock import patch

import pytest
from db.models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from tests.fixtures import common_data

engine = create_engine("sqlite:///:memory:")


@contextmanager
def db_session():
    Base.metadata.create_all(engine)
    db_session = scoped_session(sessionmaker(autocommit=False, autoflush=True, bind=engine, expire_on_commit=False))
    yield db_session
    db_session.close()


@pytest.fixture
def common_data_fixture():
    return copy.deepcopy(common_data)


def pytest_configure(config):
    mock_db_session = patch("db.queries.db_session", db_session)
    mock_db_session.start()


def pytest_runtest_teardown(item):
    from db.models import Base

    with db_session() as db:
        for table in reversed(Base.metadata.sorted_tables):
            db.execute(table.delete())
            db.commit()
