import discord
from discord import app_commands
from config.settings import settings

class Elcreat(discord.Client):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(
            command_prefix=settings.BOT_PREFIX,
            intents=intents
        )
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

    async def on_ready(self):
        print(f"O Bot {self.user} foi ligado com sucesso!")

bot = Elcreat()

bot.run(settings.BOT_TOKEN)