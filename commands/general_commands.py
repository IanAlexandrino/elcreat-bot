import discord

async def setup(bot):
    @bot.tree.command(name="teste",description="Comando para testar se o bot está online")
    async def test_command(interaction:discord.Interaction):
        await interaction.response.send_message("Estou às ordens! 🫡")

    @bot.tree.command(name="help", description="Comando que exibe todos os comandos disponíveis no bot")
    async def help_command(interaction: discord.Interaction):
        try:
            is_admin = interaction.user.guild_permissions.administrator
            
            all_commands = interaction.client.tree.get_commands()
            
            help_message = "**📚 Lista de Comandos**\n\n"
            
            for cmd in all_commands:
                requires_admin = False
                if cmd.default_permissions:
                    requires_admin = cmd.default_permissions.administrator
                
                if (is_admin and requires_admin) or not requires_admin:
                    help_message += f"• **/{cmd.name}** - {cmd.description}\n"
            
            if is_admin:
                help_message += "\n🛠️ Você está vendo todos os comandos administrativos!"
            else:
                help_message += "\n🔒 Comandos administrativos estão ocultos - apenas staff pode visualizá-los"

            await interaction.response.send_message(help_message, ephemeral=True)
            
        except Exception as e:
            await interaction.response.send_message(f"❌ Erro ao exibir ajuda: {str(e)}", ephemeral=True)
