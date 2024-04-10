from discord import Intents
from discord.ext.commands import Bot as Client

from util import Logger


class Marsi(Client):
    def __init__(self):
        super().__init__(
            intents=Intents.all(),
            command_prefix='.',
        )
        self.logger = Logger("Marsi", Logger.DEBUG)

    def _logger_test(self):
        self.logger.debug("This is debug message")
        self.logger.info("This is info message")
        self.logger.warning("This is warning message")
        self.logger.error("This is error message")
        self.logger.critical("This is critical error message")

    async def on_ready(self):
        self.logger.info(f"Logged in as {self.user} ({self.user.id})")

