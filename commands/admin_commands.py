import discord
from discord import app_commands
from database import *
from typing import Optional

async def setup(bot):
    @bot.tree.command(
            name="cadastrar-funcionario",
            description="[ADMIN] Comando para cadastrar novos funcionários",
    )
    @app_commands.default_permissions(administrator=True)
    @app_commands.describe(
        member="Membro do Discord a ser cadastrado",
        name="Nome completo do funcionário",
        role="Cargo do funcionário (ex: Marketing)",
        email="Email para contato do funcionário"
    )
    async def new_employee_command(interaction:discord.Interaction, member: discord.Member, name: str, role: str, email: str):
        try:
            if not interaction.user.guild_permissions.administrator:
                await interaction.response.send_message(
                    "❌ Você não tem permissão para usar este comando!",
                )
                return

            result = await new_employee(str(member.id), name, role, email)

            if result:
                await interaction.response.send_message(
                    f"✅ Funcionário {member.mention} cadastrado com sucesso!\n"
                    f"**Cargo:** {role}\n"
                    f"**Email:** {email}",
                )
            else:
                await interaction.response.send_message(
                    "⚠️ Este funcionário já está cadastrado!",
                )

        except Exception as e:
            await interaction.response.send_message(
                f"❌ Erro ao cadastrar: {str(e)}",
            )

    @bot.tree.command(
        name="estrelas", 
        description="[ADMIN] Comando para verificar as estrelas de um funcionário"
    )
    @app_commands.default_permissions(administrator=True)
    @app_commands.describe(
        member="Membro do Discord para visualizar as estrelas",
    )
    async def check_stars_command(interaction: discord.Interaction, member: discord.Member):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "❌ Você não tem permissão para usar este comando!",
            )
            return
        
        stars = await check_stars(str(member.id))
        if stars is not None:
            await interaction.response.send_message(f"⭐ {member.mention} tem {stars} estrelas!")
        else:
            await interaction.response.send_message("⚠️ Funcionário não encontrado ou não cadastrado.")

    @bot.tree.command(
        name="listar-funcionarios",
        description="[ADMIN] Comando para listar todos os funcionários cadastrados"
    )
    @app_commands.default_permissions(administrator=True)
    async def list_employees_command(interaction: discord.Interaction):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "❌ Você não tem permissão para usar este comando!",
            )
            return

        employees_list = await get_all_employees()

        if not employees_list:
            await interaction.response.send_message("⚠️ Não há funcionários cadastrados.")
            return

        msg = "Lista de funcionários cadastrados:\n"
        for emp in employees_list:
            emp_name = emp.get("name", "Sem nome")
            emp_role = emp.get("role", "Sem cargo")
            emp_email = emp.get("email", "Sem email")
            emp_star = emp.get("stars", "Sem estrelas")
            msg += f"• **{emp_name}** | {emp_role} | {emp_email} | ⭐{emp_star}\n"

        await interaction.response.send_message(msg)

    @bot.tree.command(
        name="retirar-estrelas",
        description="[ADMIN] Comando para retirar uma quantidade de estrelas do funcionário"
    )
    @app_commands.default_permissions(administrator=True)
    @app_commands.describe(
        member="Membro do Discord que perderá estrelas",
        quantity="Quantidade de estrelas a remover (pode ser 0.5, 1, etc.)",
        reason="Motivo da perda de estrelas"
    )
    async def remove_stars_command(interaction: discord.Interaction, member: discord.Member, quantity: float, reason: str):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "❌ Você não tem permissão para usar este comando!",
            )
            return

        new_total = await remove_stars(str(member.id), quantity, reason)
        if new_total is None:
            await interaction.response.send_message(
                "⚠️ Funcionário não encontrado ou não cadastrado."
            )
        else:
            await interaction.response.send_message(
                f"✅ {member.mention} perdeu **{quantity}** estrelas.\n"
                f"Motivo: {reason}\n"
                f"Agora ele(a) está com **{new_total}** estrelas."
            )

    @bot.tree.command(
        name="adicionar-estrelas",
        description="[ADMIN] Comando para adicionar uma quantidade de estrelas para o funcionário"
    )
    @app_commands.default_permissions(administrator=True)
    @app_commands.describe(
        member="Membro do Discord que ganhará as estrelas",
        quantity="Quantidade de estrelas a ganhar (pode ser 0.5, 1, etc.)",
        reason="Motivo do ganho de estrelas"
    )
    async def add_stars_command(interaction: discord.Interaction, member: discord.Member, quantity: float, reason: str):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "❌ Você não tem permissão para usar este comando!",
            )
            return

        new_total = await add_stars(str(member.id), quantity, reason)
        if new_total is None:
            await interaction.response.send_message(
                "⚠️ Funcionário não encontrado ou não cadastrado."
            )
        else:
            await interaction.response.send_message(
                f"✅ {member.mention} ganhou **{quantity}** estrelas.\n"
                f"Motivo: {reason}\n"
                f"Agora ele(a) está com **{new_total}** estrelas."
            )

    @bot.tree.command(
        name="atualizar-funcionario",
        description="[ADMIN] Comando para atualizar os campos de um funcionário (name, role e email)"
    )
    @app_commands.default_permissions(administrator=True)
    @app_commands.describe(
        member="Membro do Discord que será atualizado",
        name="Novo nome (opcional)",
        role="Novo cargo (opcional)",
        email="Novo email (opcional)"
    )
    async def update_employee_command(
        interaction: discord.Interaction,
        member: discord.Member,
        name: Optional[str] = None,
        role: Optional[str] = None,
        email: Optional[str] = None
    ):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "❌ Você não tem permissão para usar este comando!",
            )
            return
        
        if name is None and role is None and email is None:
            await interaction.response.send_message("⚠️ Você precisa fornecer ao menos um campo para atualizar.")
            return

        updates = {}
        if name is not None:
            updates["name"] = name
        if role is not None:
            updates["role"] = role
        if email is not None:
            updates["email"] = email

        updated_employee = await update_employee(str(member.id), updates)
        if updated_employee is None:
            await interaction.response.send_message("⚠️ Funcionário não encontrado ou não cadastrado.")
        else:
            msg = f"✅ Funcionário {member.mention} atualizado com sucesso!\n"
            if "name" in updates:
                msg += f"**Nome:** {updates['name']}\n"
            if "role" in updates:
                msg += f"**Cargo:** {updates['role']}\n"
            if "email" in updates:
                msg += f"**Email:** {updates['email']}\n"
            await interaction.response.send_message(msg)

    @bot.tree.command(
        name="desativar-funcionario",
        description="[ADMIN] Comando para desativar um funcionário, alterando seu status para 'Inativo'"
    )
    @app_commands.default_permissions(administrator=True)
    @app_commands.describe(
        member="Membro do Discord a ser desativado"
    )
    async def inactivate_employee_command(interaction: discord.Interaction, member: discord.Member):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "❌ Você não tem permissão para usar este comando!",
            )
            return
        
        updates = {"status": "Inativo"}
        
        updated_employee = await update_employee(str(member.id), updates)
        if updated_employee is None:
            await interaction.response.send_message("⚠️ Funcionário não encontrado ou não cadastrado.")
        else:
            await interaction.response.send_message(
                f"✅ Funcionário {member.mention} foi desativado com sucesso!"
            )
