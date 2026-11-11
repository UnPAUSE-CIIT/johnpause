"""Entry point: creates the bot, loads cogs, and runs it."""

import discord
from discord import app_commands
from discord.ext import commands

from config import DISCORD_TOKEN, SRV_ID
from audit import send_audit


async def on_tree_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    cmd = interaction.command.name if interaction.command else "unknown"
    await send_audit(bot, f"{interaction.user} ran `/{cmd}` -> error: {error}")

    if isinstance(error, app_commands.CheckFailure):
        msg = "You don't have permission to use that command."
    else:
        print(f"Unhandled error in /{cmd}: {error!r}")
        msg = "Something went wrong running that command."

    if interaction.response.is_done():
        await interaction.followup.send(msg, ephemeral=True)
    else:
        await interaction.response.send_message(msg, ephemeral=True)


class JohnPauseBot(commands.Bot):
    async def setup_hook(self):
        await self.load_extension("cogs.intro")
        self.tree.on_error = on_tree_error
        for cmd in self.tree.walk_commands():
            print(f'!! Registered command /{cmd.qualified_name}')


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = JohnPauseBot(command_prefix="!", intents=intents)  # prefix unused; slash commands only


@bot.event
async def on_ready():
    print(f'!! Logged in as {bot.user}')
    print(f'!! In guilds: {[(g.name, g.id) for g in bot.guilds]}')
    print(f'!! Sync target guild id from SRV_ID: {SRV_ID}')
    try:
        synced = await bot.tree.sync(guild=discord.Object(id=SRV_ID))
        print(f'!! Synced {len(synced)} commands to guild {SRV_ID}: {[c.name for c in synced]}')
    except discord.DiscordException as e:
        print(f'!! Guild sync FAILED: {e!r}')


bot.run(DISCORD_TOKEN)
