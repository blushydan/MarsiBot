import os
from pathlib import Path

from dotenv import dotenv_values


creds = dotenv_values(os.path.join(os.getcwd(), 'creds/.env'))


class LogPath:
    main = Path('logs', 'main.log')
