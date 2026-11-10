"""Entry point: creates the bot, loads cogs, and runs it."""

import discord
from discord.ext import commands

from config import DISCORD_TOKEN, SRV_ID


class JohnPauseBot(commands.Bot):
    async def setup_hook(self):
        await self.load_extension("cogs.intro")


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = JohnPauseBot(command_prefix="!", intents=intents)  # prefix unused; slash commands only


@bot.event
async def on_ready():
    await bot.tree.sync(guild=discord.Object(id=SRV_ID))
    print(f'!! Logged in as {bot.user}')


bot.run(DISCORD_TOKEN)
