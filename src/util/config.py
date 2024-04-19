import os
from pathlib import Path

from dotenv import dotenv_values


creds = dotenv_values(os.path.join(os.getcwd(), 'src/creds/.env'))


class BotConfig:
    token = creds['DISCORD_TOKEN']
    prefix = "!"


class DatabaseConfig:
    host = creds['DATABASE_HOST']
    username = creds['DATABASE_USERNAME']
    password = creds['DATABASE_PASSWORD']
    database = creds['DATABASE_NAME']

    def __repr__(self):
        return f"postgresql+asyncpg://{self.username}:{self.password}@{self.host}/{self.database}"

    def __str__(self):
        return self.__repr__()


class LogPath:
    main = Path('src', 'logs', 'main.log')
    database = Path('src', 'logs', 'database.log')
