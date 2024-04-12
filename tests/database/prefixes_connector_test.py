import sqlite3
import os

from tests.database.conftest import mocker
from pathlib import Path

from src.database.local.prefixes_connector import PrefixesConnector
import pytest


class TestPrefixesConnector:
    # Creating an instance of PrefixesConnector with no arguments should connect to the default database.
    def test_create_instance_with_no_arguments(self):
        # Act
        db = PrefixesConnector()

        # Assert
        assert db.database_path == Path('src', 'database', 'local', 'prefixes.db')
        assert isinstance(db.connection, sqlite3.Connection)

    # Creating an instance of PrefixesConnector with an invalid database path should raise an exception.
    def test_create_instance_with_invalid_database_path(self):
        # Arrange
        invalid_path = "invalid_path"

        # Act & Assert
        with pytest.raises(sqlite3.OperationalError):
            PrefixesConnector(invalid_path)

        os.remove(invalid_path)

    # Calling set_prefix() with a user_id that does not exist in the 'prefixes' table should insert a new row.
    def test_set_prefix_with_nonexistent_user_id(self):
        # Arrange
        db = PrefixesConnector(':memory:')
        db.create_table()
        user_id = 1
        prefix = "!"

        # Act
        db.set_prefix(user_id, prefix)
        result = db.get_prefix(user_id)

        # Assert
        assert result == prefix

    # Calling set_prefix() should insert or update the prefix for the user_id.
    def test_set_prefix_inserts_or_updates_prefix(self, mocker):
        # Arrange
        user_id = 1
        prefix = "!"
        db = PrefixesConnector(':memory:')
        db.create_table()

        # Act
        db.set_prefix(user_id, prefix)
        result = db.get_prefix(user_id)

        # Assert
        assert result == prefix

    # Calling get_prefix() with a user_id that has a prefix should return the prefix.
    def test_get_prefix_with_existing_prefix(self, mocker):
        # Arrange
        user_id = 1
        prefix = "!"
        db = PrefixesConnector(':memory:')
        db.create_table()
        db.set_prefix(user_id, prefix)

        # Act
        result = db.get_prefix(user_id)

        # Assert
        assert result == prefix

    # Calling get_prefix() with a user_id that does not exist should return None.
    def test_get_prefix_user_id_not_exist(self, mocker):
        # Arrange
        user_id = 123
        db = PrefixesConnector(':memory:')
        db.create_table()

        # Act
        result = db.get_prefix(user_id)

        # Assert
        assert result is None
