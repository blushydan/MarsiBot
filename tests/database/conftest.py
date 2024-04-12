import pytest

from src.database.local.prefixes_connector import PrefixesConnector


@pytest.fixture
def db():
    connector = PrefixesConnector(':memory:')
    connector.create_table()

    yield connector


@pytest.fixture
def mocker():
    from unittest.mock import Mock
    return Mock()