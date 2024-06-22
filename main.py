import pandas
import discord
from discord.ext import commands, tasks
import requests
import pybit
# import TA-lib
import datetime
import os

BOT_TOKEN = os.environ["discord-bot-token"]
DISCORD_CS = os.environ["discord-CS"]
DISCORD_APP_ID = os.environ["discord-app-id"]
CHANNEL_ID = int(os.environ["discord-testchannel-id"])


intents = discord.Intents.all()
intents.messages = True
intents.guilds = True
bot = commands.Bot(command_prefix='!', intents=intents)


# Test: Send time message every minute
# @tasks.loop(minutes=1)
@tasks.loop(hours=1)
async def send_time_message():
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    channel = bot.get_channel(CHANNEL_ID)  # Replace with your channel ID
    await channel.send(f'Current server time is: {current_time}')


# Event: Bot is ready
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    send_time_message.start()  # Start the task when the bot is ready


# Run the bot
bot.run(BOT_TOKEN)
