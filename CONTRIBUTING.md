# Contributing to JohnPAUSE

Thanks for wanting to help! This is an open source project for our game development org, and the main ways to contribute are through **Issues** and **Pull Requests**.

## Ground rules

- **@zsfer must be set as reviewer on every Pull Request.** This is enforced via `.github/CODEOWNERS`, which auto-requests them on all PRs. Please do not remove them as a reviewer or merge without their approval.
- **This bot is hosted on sillydev, so keeping it lightweight is super important.** Keep dependencies to the absolute minimum and avoid bloat: no databases, no web servers, no background jobs unless absolutely necessary.
- Keep the code simple. Officers with basic Python knowledge should be able to read and extend this codebase.
- Everything goes through Issues and PRs. Don't push straight to `master`.

## Contributing via Issues

- Found a bug or want a new feature? Open an Issue first so we can discuss it before work starts.
- Search existing Issues to avoid duplicates.
- Include what you expected to happen, what actually happened, and steps to reproduce (for bugs).

## Contributing via Pull Requests

1. Fork the repo and clone your fork.
2. Create a branch for your change: `git checkout -b my-change`.
3. Make your changes. Keep PRs small and focused - one feature or fix per PR.
4. Test locally first: `python app.py` and make sure the bot still logs in and behaves.
5. Use [Conventional Commits](https://www.conventionalcommits.org/) for your commit messages, e.g. `feat: add ...`, `fix: ...`, `docs: ...`.
6. Push your branch and open a PR against `master`.
7. **Make sure @zsfer is set as a reviewer on the PR.** CODEOWNERS does this automatically - leave it as is.
8. Wait for review. Don't merge your own PR without zsfer's approval.

## Project layout

- `app.py` - entry point: creates the bot, loads cogs, runs it
- `config.py` - environment loading and validation
- `audit.py` - posts command audit logs to `AUDIT_CHNL`
- `cogs/` - one cog per feature; copy `cogs/intro.py` as a starting point
- `.env.example` - template for the required environment variables

## Adding a new cog

1. Create `cogs/myfeature.py` with a `commands.Cog` subclass and an `async def setup(bot)` function.
2. Add `await self.load_extension("cogs.myfeature")` in `JohnPauseBot.setup_hook` in `app.py`.
3. Every command must call `send_audit` from `audit.py` to log who ran it and what happened. Command errors are audit logged automatically by the global error handler in `app.py`.

## Style notes

- Simple, readable Python over clever abstractions.
- No new dependencies without a strong reason - the bot has to stay lightweight for sillydev hosting.
- Don't commit `.env` or any secrets. It's gitignored; keep it that way.
