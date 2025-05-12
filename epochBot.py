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
    app_commands.Choice(name="Relative (in ...)", value="R"),   # <t:epoch:R>
    app_commands.Choice(name="Short Time", value="t"),
    app_commands.Choice(name="Long Time", value="T"),
    app_commands.Choice(name="Short Date", value="d"),
    app_commands.Choice(name="Long Date", value="D"),
    app_commands.Choice(name="Short DateTime", value="f"),
    app_commands.Choice(name="Long DateTime", value="F"),
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
    datetime_str="Format: YYYY-MM-DD HH:MM:SS (24h)",
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
        dt = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
        localized_dt = user_tz.localize(dt)
        seconds = int(localized_dt.timestamp())
        fmt = format.value if format else "R"
        countdown_msg = f"{pre_msg} <t:{seconds}:{fmt}> {post_msg}".strip()
        await interaction.response.send_message(countdown_msg)
    except Exception as e:
        await interaction.response.send_message(f"❌ Error: {e}")

client.run(TOKEN)
"""
https://discord.com/oauth2/authorize?client_id=1371199566749237492&permissions=274877908992&integration_type=0&scope=bot+applications.commands
"""
