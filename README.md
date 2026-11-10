# johnpause

A small Discord bot that syncs the server's #intro channel to member nicknames.

- Watching #intro: anyone who posts in the intro channel gets their nickname set to their message content.
- `/checkusersinintro`: manually set the nick of the latest #intro poster (requires Manage Nicknames).

## Setup

1. Create a virtual environment and install dependencies:

   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env` and fill in:

   - `DISCORD_TOK` — bot token from the Discord developer portal
   - `SRV_ID` — ID of your server (guild)
   - `INTRO_CHNL` — ID of the #intro channel

   The bot exits with a clear error at startup if any of these are missing or invalid.

3. Run the bot:

   ```powershell
   python app.py
   ```

## Project layout

- `app.py` — the bot itself (single file)
- `config.py` — environment loading and validation
- `.env.example` — template for required environment variables
- `requirements.txt` — Python dependencies
