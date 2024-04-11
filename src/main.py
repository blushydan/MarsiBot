import coloredlogs

from bot import Marsi
from util.config import creds


coloredlogs.install(level='DEBUG')


def main():
    bot = Marsi()
    bot.run(token=creds['DISCORD_TOKEN'], log_level='WARNING')


if __name__ == '__main__':
    main()
