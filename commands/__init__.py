from .admin_commands import setup as admin_setup
from .general_commands import setup as general_setup

async def setup(bot):
    await admin_setup(bot)
    await general_setup(bot)