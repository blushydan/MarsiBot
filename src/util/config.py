import os
from pathlib import Path

from dotenv import dotenv_values


creds = dotenv_values(os.path.join(os.getcwd(), 'src/creds/.env'))


class BotConfig:
    token = creds['DISCORD_TOKEN']
    prefix = "!"


class LogPath:
    main = Path('src', 'logs', 'main.log')
    database = Path('src', 'logs', 'database.log')
