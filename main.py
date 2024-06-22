import pandas
import discord
from discord.ext import commands
import requests
import pybit
# import TA-lib
import datetime
import os

BOT_TOKEN = os.environ["discord-bot-token"]
DISCORD_CS = os.environ["discord-CS"]
DISCORD_APP_ID = os.environ["discord-app-id"]


intents = discord.Intents.all()
intents.messages = True  # You can add more intents as needed
bot = commands.Bot(command_prefix='!', intents=intents)

# Event: Bot is ready
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

# Command: Get current time
@bot.command(name='time', help='Responds with the current time')
async def current_time(ctx):
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    await ctx.send(f'Current server time is: {current_time}')

# Run the bot
bot.run(BOT_TOKEN)


