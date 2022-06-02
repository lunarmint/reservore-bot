import logging

import discord
from discord.ext import commands

from modules.config import config
from modules.utils import embeds

log = logging.getLogger(__name__)


class RoleSelector(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="roleselector")
    async def role_selector(self, ctx: commands.Context):
        role_assignment_text = f"""
        You can react to one of the emotes below to assign yourself a positional role.
        🔍  <@&{config["roles"]["foh"]}> - Front of House
        🍖  <@&{config["roles"]["boh"]}> - Back of House
        """
        roles = {
            "🔍": config["roles"]["foh"],
            "🍖": config["roles"]["boh"],
        }

        embed = embeds.make_embed(description=role_assignment_text, color=discord.Color.blurple())
        msg = await ctx.send(embed=embed)
        for key, value in roles.items():
            await msg.add_reaction(key)


def setup(bot: commands.Bot):
    bot.add_cog(RoleSelector(bot))
    log.info("Command loaded: role_selector")
