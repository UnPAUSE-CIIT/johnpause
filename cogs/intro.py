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
            await send_audit(self.bot, f"{user} ran `/checkusersinintro` -> failed: #intro channel not found")
            return

        async for m in chnl.history(limit=count):
            await self.__update_nick(interaction, m)

    async def __update_nick(self, interaction: discord.Interaction, m: discord.Message):
        user = interaction.user
        if m.author.bot:
            await interaction.response.send_message(
                "Latest message in #intro is from a bot; nothing to do.", ephemeral=True
            )
            await send_audit(self.bot, f"{user} ran `/checkusersinintro` -> no-op: latest message is from a bot")
            return
        if m.author is not discord.Member:
            await interaction.response.send_message(
                "User is not a member; nothing to do.", ephemeral=True
            )
            await send_audit(self.bot, f"{user} ran `/checkusersinintro` -> no-op: user is not a member")
            return

        m.author.edit(nick=m.content)
        msg = f"Set {m.author}'s nick to `{m.content}`"
        await interaction.response.send_message(msg, ephemeral=True)
        await send_audit(self.bot, f"{user} ran `/checkusersinintro` -> set {m.author}'s nick to `{m.content}`")

async def setup(bot: commands.Bot): await bot.add_cog(Intro(bot))
