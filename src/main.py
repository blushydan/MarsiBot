import coloredlogs

from src.bot import Marsi
from src.util.config import BotConfig


coloredlogs.install(level='DEBUG')


def main():
    bot = Marsi()
    bot.run(token=BotConfig.token, log_level='WARNING')


if __name__ == '__main__':
    main()
