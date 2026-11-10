"""Environment configuration loading and validation.

Reads variables from .env (if present) and the process environment,
and fails fast with a clear message when something required is missing.
"""

import os

from dotenv import load_dotenv

load_dotenv()


def _required(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(
            f"Missing required environment variable: {name}. "
            "Copy .env.example to .env and fill it in."
        )
    return value


def _required_int(name: str) -> int:
    raw = _required(name)
    try:
        return int(raw)
    except ValueError:
        raise RuntimeError(f"{name} must be an integer, got {raw!r}") from None


DISCORD_TOKEN = _required("DISCORD_TOK")
SRV_ID = _required_int("SRV_ID")
INTRO_CHNL = _required_int("INTRO_CHNL")
