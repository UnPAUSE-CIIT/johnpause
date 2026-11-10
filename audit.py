"""Audit logging: posts what the bot does to a configured channel."""

import discord

from config import AUDIT_CHNL


async def send_audit(bot: discord.Client, message: str) -> None:
    channel = bot.get_channel(AUDIT_CHNL)
    if channel is None:
        try:
            channel = await bot.fetch_channel(AUDIT_CHNL)
        except discord.DiscordException as e:
            print(f"audit log: could not fetch channel {AUDIT_CHNL}: {e}")
            return
    await channel.send(f"📜 {message}", allowed_mentions=discord.AllowedMentions.none())
