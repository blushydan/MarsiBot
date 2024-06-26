import os
import time

from discord import Intents
from discord.ext import commands

from src.util import Logger, DatabaseConfig
from src.bot.prefix import determine_prefix
from src.database.connector import DatabaseConnector


class Marsi(commands.Bot):
    instance: "Marsi"

    def __new__(cls, *args, **kwargs):  # Singleton pattern
        if not hasattr(cls, "instance"):
            cls.instance = super(Marsi, cls).__new__(cls)

        return cls.instance

    def __init__(self):
        self.logger = Logger("Marsi", Logger.DEBUG)
        self.start_time = time.time()  # Used to calculate bot startup time
        super().__init__(
            intents=Intents.all(),
            command_prefix=commands.when_mentioned_or(determine_prefix),
        )
        DatabaseConnector.initialize(str(DatabaseConfig()), echo=False)

    def _logger_test(self):
        self.logger.debug("This is debug message")
        self.logger.info("This is info message")
        self.logger.warning("This is warning message")
        self.logger.error("This is error message")
        self.logger.critical("This is critical error message")

    async def setup_hook(self) -> None:
        cogs = [file for file in os.listdir("src/cogs") if file.endswith(".py")]  # Get all cog files
        for cog in cogs:
            await self.load_extension(f"src.cogs.{cog[:-3]}")  # Load each cog

    async def on_ready(self):
        self.logger.info(f"Logged in as {self.user} ({self.user.id})")
        self.logger.info(f"Bot started in {time.time() - self.start_time:.2f} seconds")

    @classmethod
    def get_bot(cls) -> "Marsi":
        return cls.instance
