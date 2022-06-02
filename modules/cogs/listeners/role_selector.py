import logging

import discord
from discord.ext import commands

from modules.config import config
from modules.utils import embeds

log = logging.getLogger(__name__)


class RoleSelectorListener(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        channel_roles = self.bot.get_channel(payload.channel_id)
        channel_general = self.bot.get_channel(config["channels"]["general"])
        message = await channel_roles.fetch_message(payload.message_id)

        if message.id != config["embeds"]["role_selector"] or payload.member.bot:
            return

        guild = self.bot.get_guild(payload.guild_id)
        foh = discord.utils.get(guild.roles, id=config["roles"]["foh"])
        boh = discord.utils.get(guild.roles, id=config["roles"]["boh"])
        roles = {
            "🔍": foh,
            "🍖": boh,
        }

        role_name_shorthanded = {
            "Service - ": foh,
            "Kitchen - ": boh,
        }

        for key, role in roles.items():
            # If the reaction and the emote on the embed is the same.
            if key == payload.emoji.name:
                # Remove the role if they already have them, or otherwise.
                if role in payload.member.roles:
                    await payload.member.remove_roles(role)
                    await self.remove_nickname(payload.member, role_name_shorthanded)
                else:
                    await payload.member.add_roles(role)
                    embed = embeds.make_embed(
                        description=f"<@{payload.member.id}>, welcome to <@&{role.id}>!", color=discord.Color.blurple()
                    )
                    await channel_general.send(embed=embed)
                    await self.update_nickname(payload.member, role, role_name_shorthanded)
            # Remove other roles to make sure the selected role is unique.
            elif role in payload.member.roles:
                await payload.member.remove_roles(role)

        # Finally, remove the reaction.
        await message.remove_reaction(payload.emoji, payload.member)

    @staticmethod
    async def remove_nickname(member: discord.Member, role_name_shorthanded: dict):
        name = member.display_name
        for key, value in role_name_shorthanded.items():
            if key in name:
                await member.edit(nick=name.replace(key, ""))

    @staticmethod
    async def update_nickname(member: discord.Member, role: discord.Role, role_name_shorthanded: dict):
        name = member.display_name
        for key, value in role_name_shorthanded.items():
            if key in name:
                name = name.replace(key, "")

        for key, value in role_name_shorthanded.items():
            if role == value:
                await member.edit(nick=f"{key}{name}")


def setup(bot: commands.Bot):
    bot.add_cog(RoleSelectorListener(bot))
    log.info("Listener loaded: role_selector")
