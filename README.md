# JohnPAUSE. the bot of John UnPAuse

## Setup

1. Create a virtual environment and install dependencies:

   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env` and fill in:

   - `DISCORD_TOK` — bot token from the Discord developer portal. ask seifer
   - `SRV_ID` — ID of your server (guild). ask seifer
   - `INTRO_CHNL` — ID of the #intro channel, used to update new usersname

   The bot exits with a clear error at startup if any of these are missing or invalid.

3. Run the bot:

   ```powershell
   python app.py
   ```

## Project layout

- `app.py` — entry point: creates the bot, loads cogs, runs it
- `config.py` — environment loading and validation
- `cogs/intro.py` — intro channel nickname sync (listener + `/checkusersinintro`)
- `.env.example` — template for required environment variables
- `requirements.txt` — Python dependencies

## Adding a new cog

1. Create `cogs/myfeature.py` with a `commands.Cog` subclass and an `async def setup(bot)` function.
2. Add `await self.load_extension("cogs.myfeature")` in `JohnPauseBot.setup_hook` in `app.py`.
