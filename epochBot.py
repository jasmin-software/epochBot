import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime
import os
import pytz
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
client = commands.Bot(command_prefix="!", intents=intents)

# Define choices for timezones
timezone_choices = [
    app_commands.Choice(name="UTC", value="UTC"),
    app_commands.Choice(name="Vancouver (America/Vancouver)",
                        value="America/Vancouver"),
    app_commands.Choice(name="Brunei (Asia/Brunei)", value="Asia/Brunei"),
]

# Define choices for Discord timestamp formats
format_choices = [
    app_commands.Choice(
        name="Relative (in 420 days)", value="R"),   # <t:epoch:R>
    app_commands.Choice(name="Short Time (16:20)", value="t"),
    app_commands.Choice(name="Long Time (16:20:30)", value="T"),
    app_commands.Choice(name="Short Date (20/04/2021)", value="d"),
    app_commands.Choice(name="Long Date (20 April 2021)", value="D"),
    app_commands.Choice(
        name="Short DateTime (20 April 2021 16:20)", value="f"),
    app_commands.Choice(
        name="Long DateTime (Tuesday, 20 April 2021 16:20)", value="F"),
]


@client.event
async def on_ready():
    print(f"Logged in as {client.user} (ID: {client.user.id})")
    try:
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")


@client.tree.command(name="epoch", description="Create a countdown timestamp message")
@app_commands.choices(
    timezone=timezone_choices,
    format=format_choices
)
@app_commands.describe(
    pre_msg="Message before the countdown",
    datetime_str="Format: YYYY-MM-DD HH:MM:SS (24h, time is optional)",
    timezone="Your timezone",
    format="Timestamp display format (default: Relative)",
    post_msg="Message after the countdown"
)
async def epoch(
    interaction: discord.Interaction,
    pre_msg: str,
    datetime_str: str,
    timezone: app_commands.Choice[str],
    format: app_commands.Choice[str] = None,
    post_msg: str = ""
):
    try:
        user_tz = pytz.timezone(timezone.value)
        dt = generate_unix_time(datetime_str)
        # dt = datetime.strptime(datetime, "%Y-%m-%d %H:%M:%S")
        localized_dt = user_tz.localize(dt)
        seconds = int(localized_dt.timestamp())
        fmt = format.value if format else "R"
        countdown_msg = f"{pre_msg} <t:{seconds}:{fmt}>{post_msg}".strip()
        await interaction.response.send_message(countdown_msg)
    except Exception as e:
        await interaction.response.send_message(f"❌ Error: {e}")


def generate_unix_time(datetime_str):
    formats = [
        "%Y-%m-%d %H:%M:%S",  # Full format with seconds
        "%Y-%m-%d %H:%M",     # Without second
        "%Y-%m-%d %H",        # Without minute
        "%Y-%m-%d",           # Without hour
    ]
    for fmt in formats:
        try:
            dt = datetime.strptime(datetime_str, fmt)
            break
        except Exception as e:
            # print(f"{fmt} is not valid for input {e}")
            continue
    return dt


client.run(TOKEN)
# test = generate_unix_time("2023-10-01 12:00:00")
# test = generate_unix_time("2023-10-01 12:00")
# test = generate_unix_time("2023-10-01 12")
# test = generate_unix_time("2023-10-01")
# test = generate_unix_time("2023-10-01")
