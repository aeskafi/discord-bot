<div align="center">

# 🤖 Discord Bot

**An intelligent, lightweight Discord assistant for automated inspiration, custom encouragements, and scheduled asynchronous reminders.**

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![discord.py](https://img.shields.io/badge/discord.py-v2.3+-5865F2?style=flat-square&logo=discord&logoColor=white)](https://discordpy.readthedocs.io/)
[![Flask](https://img.shields.io/badge/Flask-Keep--Alive-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](./LICENSE)

<p align="center">
  A self-contained Discord bot designed to keep your community motivated, provide daily wisdom, and dispatch non-blocking reminders with zero hassle.
</p>

</div>

---

## ⚡ Key Features

- 🧠 **Dynamic Sentiment Cheer-Up**: Automatically detects downhearted keywords (`sad`, `depressed`, `unhappy`, `angry`) and offers random words of encouragement.
- 📜 **ZenQuotes API Integration**: Fetches fresh quotes and author attributions on demand, complete with offline fallback quotes.
- ⏰ **Asynchronous Reminder Scheduler**: Set reminders with human duration syntax (`10s`, `5m`, `2h`, `1d`) that run concurrently via non-blocking `asyncio` timers.
- 💾 **Universal Dual-Storage Backend**: Seamlessly uses **Replit DB** when hosted on Replit, and falls back to a clean local JSON storage adapter for VPS, Docker, or local environments.
- 🌐 **Built-In Keep-Alive Server**: Integrated background Flask daemon on port `8080` (or custom `$PORT`) for 24/7 uptime monitoring via services like UptimeRobot or BetterUptime.

---

## 📋 Command Reference

| Command | Arguments | Description | Example |
|---|---|---|---|
| `!help` | None | Displays the bot commands and quick reference guide | `!help` |
| `!inspire` | None | Fetches an inspiring quote from ZenQuotes | `!inspire` |
| `!add` | `<message>` | Adds a custom encouraging message to the database | `!add Keep shipping daily!` |
| `!del` | `<index>` | Deletes an encouragement by its numeric index | `!del 0` |
| `!list` | None | Displays all saved custom encouragements | `!list` |
| `!responding` | `<true\|false>` | Toggles automatic responses to sad keywords | `!responding true` |
| `!remind` | `<duration> <message>` | Schedules a channel reminder alert | `!remind 15m review PR #42` |

---

## 🚀 Quickstart

### 1. Clone & Set Up Virtual Environment

```bash
git clone https://github.com/aeskafi/discord-bot.git
cd discord-bot

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file from the provided example:

```bash
cp .env.example .env
```

Edit `.env` and supply your Discord Bot Token from the [Discord Developer Portal](https://discord.com/developers/applications):

```ini
DISCORD_TOKEN=your_discord_bot_token_here
PORT=8080
```

> **Note**: Ensure the **Message Content Intent** is enabled under the **Bot** tab in your Discord Developer Application settings.

### 3. Run the Bot & Test Suite

```bash
# Run the Discord Bot
python main.py

# Run the automated unit test suite
python -m unittest discover tests
```

---

## 📁 Repository Structure

```text
discord-bot/
├── main.py              # Core Discord client, commands & event handling
├── storage.py           # Unified Replit DB & LocalStorage JSON adapter
├── keep_alive.py        # Background Flask web health check service
├── requirements.txt     # Python production & testing dependencies
├── pyproject.toml       # Poetry package manifest & tool configuration
├── .env.example         # Example environment configuration
├── tests/
│   └── test_bot.py      # Automated unit tests for storage & command parsers
└── README.md            # Project documentation & reference
```

---

## 👨‍💻 Author & Mission

Created by **[Arham Eskafi](https://arham.dev)** — Rapid MVP Specialist and creator documenting life on the road as an overland tech nomad on **[Walk Cook Live](https://youtube.com/@walkcooklive)**.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).