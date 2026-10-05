import os
import sys
import json
import random
import asyncio
from datetime import datetime, timezone
import requests

try:
    import discord
except ImportError:
    discord = None
from storage import get_db
from keep_alive import keep_alive

# Initialize database storage adapter (Replit DB or LocalStorage)
db = get_db()

# Default sadness triggers and encouraging messages
SAD_WORDS = ["sad", "depressed", "unhappy", "angry", "miserable", "depressing"]

STARTER_ENCOURAGEMENTS = [
    "Cheer up!",
    "Hang in there.",
    "You are a great person / bot!",
    "Every day is a fresh start — keep moving forward!",
    "You've got this! Take a deep breath and keep building."
]

if "responding" not in db.keys():
    db["responding"] = True


def get_quote() -> str:
    """Fetch an inspiring quote from ZenQuotes with local fallback."""
    try:
        response = requests.get("https://zenquotes.io/api/random", timeout=5)
        if response.status_code == 200:
            json_data = response.json()
            if json_data and isinstance(json_data, list):
                return f"{json_data[0]['q']} — {json_data[0]['a']}"
    except Exception as e:
        print(f"[Quote Fetch Warning] {e}")

    fallback_quotes = [
        "The best way to get started is to quit talking and begin doing. — Walt Disney",
        "Don't let yesterday take up too much of today. — Will Rogers",
        "It's not whether you get knocked down, it's whether you get up. — Vince Lombardi",
        "Code is like humor. When you have to explain it, it's bad. — Cory House"
    ]
    return random.choice(fallback_quotes)


def update_encouragements(encouraging_message: str):
    """Add a new encouraging message to storage."""
    encouragements = list(db.get("encouragements", []))
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements


def delete_encouragement(index: int) -> bool:
    """Delete an encouraging message by its 0-based index."""
    encouragements = list(db.get("encouragements", []))
    if 0 <= index < len(encouragements):
        encouragements.pop(index)
        db["encouragements"] = encouragements
        return True
    return False


def parse_duration(time_str: str) -> tuple[int, str]:
    """Parse time string like 10s, 5m, 2h, 1d into seconds and human description."""
    time_str = time_str.strip().lower()
    if not time_str or len(time_str) < 2:
        return 0, ""
    unit = time_str[-1]
    value_str = time_str[:-1]

    if not value_str.isdigit():
        return 0, ""

    val = int(value_str)
    if unit == "s":
        return val, f"{val} second(s)"
    elif unit == "m":
        return val * 60, f"{val} minute(s)"
    elif unit == "h":
        return val * 3600, f"{val} hour(s)"
    elif unit == "d":
        return val * 86400, f"{val} day(s)"
    return 0, ""


# Configure Discord client with modern message_content intents
if discord:
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f"Logged in successfully as {client.user} (ID: {client.user.id if client.user else 'Unknown'})")
        print(f"Serving commands: !inspire, !add, !del, !list, !responding, !remind, !help")

    @client.event
    async def on_message(message: discord.Message):
        if message.author == client.user:
            return

        msg = message.content.strip()

        # !help command
        if msg.startswith("!help"):
            embed = discord.Embed(
                title="🤖 Discord Bot Commands",
                description="Your personal inspiration and reminder assistant.",
                color=0x3b82f6,
                timestamp=datetime.now(timezone.utc)
            )
            embed.add_field(name="!inspire", value="Fetch an inspiring daily quote", inline=False)
            embed.add_field(name="!add <message>", value="Save a custom encouraging message", inline=False)
            embed.add_field(name="!del <index>", value="Delete an encouragement by index", inline=False)
            embed.add_field(name="!list", value="List all saved custom encouragements", inline=False)
            embed.add_field(name="!responding <true/false>", value="Toggle automatic cheer-up responses", inline=False)
            embed.add_field(name="!remind <duration> <message>", value="Set a reminder (e.g. `!remind 10m check oven`)", inline=False)
            embed.set_footer(text="Created by Arham Eskafi (arham.dev)")
            await message.channel.send(embed=embed)
            return

        # !inspire command
        if msg.startswith("!inspire"):
            quote = get_quote()
            await message.channel.send(f"“ {quote} ”")
            return

        # Automatic cheer-up responses for sad keywords
        if db.get("responding", True):
            options = list(STARTER_ENCOURAGEMENTS)
            options.extend(list(db.get("encouragements", [])))
            if any(word in msg.lower().split() for word in SAD_WORDS):
                await message.channel.send(random.choice(options))

        # !add command
        if msg.startswith("!add"):
            parts = msg.split("!add", 1)
            if len(parts) > 1 and parts[1].strip():
                encouraging_message = parts[1].strip()
                update_encouragements(encouraging_message)
                await message.channel.send(f"✅ Added new encouragement: *\"{encouraging_message}\"*")
            else:
                await message.channel.send("⚠️ Usage: `!add <your encouraging message>`")
            return

        # !del command
        if msg.startswith("!del"):
            parts = msg.split("!del", 1)
            if len(parts) > 1 and parts[1].strip().isdigit():
                index = int(parts[1].strip())
                if delete_encouragement(index):
                    await message.channel.send(f"🗑️ Deleted encouragement at index {index}.")
                else:
                    await message.channel.send(f"⚠️ Index {index} not found in database. Use `!list` to view valid indices.")
            else:
                await message.channel.send("⚠️ Usage: `!del <number_index>` (e.g. `!del 0`)")
            return

        # !list command
        if msg.startswith("!list"):
            encouragements = list(db.get("encouragements", []))
            if not encouragements:
                await message.channel.send("📭 No custom encouragements saved yet. Use `!add <message>` to add one.")
            else:
                formatted = "\n".join(f"`[{i}]` {item}" for i, item in enumerate(encouragements))
                await message.channel.send(f"**Saved Encouragements:**\n{formatted}")
            return

        # !responding toggle
        if msg.startswith("!responding"):
            parts = msg.split("!responding", 1)
            if len(parts) > 1:
                val_str = parts[1].strip().lower()
                if val_str == "true":
                    db["responding"] = True
                    await message.channel.send("🟢 Automatic responding is now **ON**.")
                elif val_str == "false":
                    db["responding"] = False
                    await message.channel.send("🔴 Automatic responding is now **OFF**.")
                else:
                    await message.channel.send("⚠️ Usage: `!responding true` or `!responding false`")
            return

        # !remind command: !remind <duration> <message>
        if msg.startswith("!remind"):
            parts = msg.split(maxsplit=2)
            avatar_url = client.user.display_avatar.url if client.user else None

            embed = discord.Embed(color=0x55a7f7, timestamp=datetime.now(timezone.utc))
            if avatar_url:
                embed.set_footer(text="Discord Bot by Arham Eskafi (arham.dev)", icon_url=avatar_url)
            else:
                embed.set_footer(text="Discord Bot by Arham Eskafi (arham.dev)")

            if len(parts) < 3:
                embed.add_field(
                    name="⚠️ Usage Error",
                    value="Format: `!remind <duration> <message>`\nExample: `!remind 10m check deploy` or `!remind 2h gym session`"
                )
                await message.channel.send(embed=embed)
                return

            time_str, reminder_text = parts[1], parts[2]
            seconds, human_duration = parse_duration(time_str)

            if seconds <= 0:
                embed.add_field(
                    name="⚠️ Invalid Duration",
                    value="Please specify valid duration suffix: `s` (seconds), `m` (minutes), `h` (hours), or `d` (days).\nExample: `!remind 30m team sync`"
                )
                await message.channel.send(embed=embed)
                return

            if seconds > 7776000:  # 90 days
                embed.add_field(name="⚠️ Duration Too Long", value="Maximum supported reminder duration is 90 days.")
                await message.channel.send(embed=embed)
                return

            await message.channel.send(f"⏰ Got it {message.author.mention}! I will remind you about **\"{reminder_text}\"** in **{human_duration}**.")
            await asyncio.sleep(seconds)
            await message.channel.send(f"🔔 {message.author.mention} **Reminder:** {reminder_text} *(set {human_duration} ago)*")
else:
    client = None


def main():
    token = os.getenv("DISCORD_TOKEN") or os.getenv("TOKEN")
    if not token:
        print("[Error] Discord bot token is missing!")
        print("Please set the DISCORD_TOKEN environment variable (or copy .env.example to .env).")
        sys.exit(1)

    # Launch background keep-alive web server
    keep_alive()

    # Run Discord client
    client.run(token)


if __name__ == "__main__":
    main()