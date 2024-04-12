from discord.ext import commands


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_load(self) -> None:
        self.bot.logger.debug("Admin cog loaded")

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.bot.latency * 1000)}ms')


async def setup(bot):
    await bot.add_cog(Admin(bot))