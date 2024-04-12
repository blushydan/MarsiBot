import sqlite3
from pathlib import Path

from src.util import Logger
from src.util.config import LogPath


class PrefixesConnector:
    database_path = Path('src', 'database', 'local', 'prefixes.db')
    logger = Logger("PrefixesConnector", Logger.DEBUG, LogPath.database)
    connection: sqlite3.Connection

    def __init__(self, database_path: Path | str | None = None):
        self.database_path = database_path if database_path else self.database_path
        self._check_if_path_is_valid()
        self.connection = sqlite3.connect(self.database_path)

    def __del__(self):
        if getattr(self, 'connection', None):
            self.connection.close()

    def _check_if_path_is_valid(self) -> None:
        if isinstance(self.database_path, Path) and self.database_path.exists():
            return
        if isinstance(self.database_path, str) and (self.database_path[:-2] == '.db' or self.database_path == ':memory:'):
            return
        raise sqlite3.OperationalError("Database path is invalid")

    def create_table(self) -> None:
        try:
            cursor = self.connection.cursor()
            cursor.execute('CREATE TABLE IF NOT EXISTS prefixes (user_id INTEGER PRIMARY KEY, prefix TEXT)')
            self.connection.commit()
            cursor.close()
        except sqlite3.Error as e:
            self.logger.exception("Error creating table")

    def get_prefix(self, user_id: int) -> str:
        try:
            cursor = self.connection.cursor()
            cursor.execute('SELECT prefix FROM prefixes WHERE user_id = ?', (user_id,))
            prefix = cursor.fetchone()
            cursor.close()
            return prefix[0] if prefix else None
        except sqlite3.Error as e:
            self.logger.exception("Error getting prefix")

    def set_prefix(self, user_id: int, prefix: str) -> None:
        try:
            cursor = self.connection.cursor()
            cursor.execute('INSERT OR REPLACE INTO prefixes (user_id, prefix) VALUES (?, ?)', (user_id, prefix))
            self.connection.commit()
            cursor.close()
        except sqlite3.Error as e:
            self.logger.exception("Error setting prefix")
