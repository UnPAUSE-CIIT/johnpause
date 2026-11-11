"""Intro channel cog: syncs nicknames from messages posted in #intro."""

import discord
from discord import app_commands
from discord.ext import commands

from audit import send_audit
from config import INTRO_CHNL


class Intro(commands.Cog):
    """Sets member nicknames to their latest #intro message."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        if not msg.guild or msg.author.bot:
            return

        if msg.channel.id == INTRO_CHNL and isinstance(msg.author, discord.Member):
            await msg.author.edit(nick=msg.content)

    @app_commands.command(
        name="sync_nicknames", description="Sync nicknames of the last N messages in #intro"
    )
    @app_commands.describe(count="Message Count")
    @app_commands.checks.has_permissions(manage_nicknames=True)
    async def sync_nicknames(self, interaction: discord.Interaction, count: int):
        if interaction.guild is None:
            return

        user = interaction.user
        chnl = interaction.guild.get_channel(INTRO_CHNL)
        if chnl is None:
            await interaction.response.send_message("#intro channel not found.", ephemeral=True)
            await send_audit(self.bot, f"{user} ran `/sync_nicknames` -> failed: #intro channel not found")
            return

        ok_count = 0
        async for m in chnl.history(limit=count):
            ok = await self._update_nick(user, m)
            if ok:
                ok_count += 1

        await interaction.response.send_message(f"Updated {ok_count} usernames :P", ephemeral=True)

    async def _update_nick(self, user: discord.abc.User, m: discord.Message) -> bool:
        if m.author.bot:
            await send_audit(self.bot, f"{user} ran `/sync_nicknames` -> no-op: {m.author} is a bot")
            return False

        member = m.author
        if not isinstance(member, discord.Member):
            await send_audit(self.bot, f"{user} ran `/sync_nicknames` -> no-op: {member} is not a member")
            return FAlse

        try:
            await member.edit(nick=m.content)
        except discord.DiscordException as e:
            await send_audit(self.bot, f"{user} ran `/sync_nicknames` -> failed on {member}: {e}")
            return False

        await send_audit(self.bot, f"{user} ran `/sync_nicknames` -> set {member}'s nick to `{m.content}`")
        return True


async def setup(bot: commands.Bot): await bot.add_cog(Intro(bot))
