import discord

from config import DISCORD_TOKEN, INTRO_CHNL, SRV_ID

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(bot)

intro_channel_id = INTRO_CHNL


@bot.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=SRV_ID))
    print(f'!! Logged in as {bot.user}')


@bot.event
async def on_message(msg):
    if not msg.guild or msg.author.bot:
        return

    if msg.channel.id == intro_channel_id and isinstance(msg.author, discord.Member):
        await msg.author.edit(nick=msg.content)


@tree.command(name="checkusersinintro", description="Set nick of latest message in #intro")
@discord.app_commands.checks.has_permissions(manage_nicknames=True)
async def cmd_check_users_in_intro(interaction: discord.Interaction):
    chnl = interaction.guild.get_channel(intro_channel_id)
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


bot.run(DISCORD_TOKEN)
