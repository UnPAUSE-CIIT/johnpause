"""Intro channel cog: syncs nicknames from messages posted in #intro."""

import discord
from discord import app_commands
from discord.ext import commands

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
        name="checkusersinintro", description="Set nick of latest message in #intro"
    )
    @app_commands.checks.has_permissions(manage_nicknames=True)
    async def check_users_in_intro(self, interaction: discord.Interaction):
        chnl = interaction.guild.get_channel(INTRO_CHNL)
        if chnl is None:
            await interaction.response.send_message("#intro channel not found.", ephemeral=True)
            return

        async for m in chnl.history(limit=1):
            if m.author.bot:
                await interaction.response.send_message(
                    "Latest message in #intro is from a bot; nothing to do.", ephemeral=True
                )
                return
            await m.author.edit(nick=m.content)
            msg = f"Set {m.author}'s nick to `{m.content}`"
            await interaction.response.send_message(msg, ephemeral=True)
            print(msg)
            return

        await interaction.response.send_message("#intro is empty.", ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(Intro(bot))
