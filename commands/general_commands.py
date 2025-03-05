import discord

async def setup(bot):
    @bot.tree.command(name="teste",description="Comando para testar se o bot está online")
    async def test(interaction:discord.Interaction):
        await interaction.response.send_message("Estou às ordens! 🫡")
