import pandas
import discord
from discord.ext import commands, tasks
import requests
import pybit
# import TA-lib
import datetime
import os
import asyncio
from discord_bot_manager import DiscordBotManager


async def trigger_send_message(bot):
    while True:
        await bot.send_time_message()
        await asyncio.sleep(5)


async def main():
    BOT_TOKEN = os.environ["discord-bot-token"]
    intents = discord.Intents.all()
    intents.messages = True
    intents.guilds = True

    bot = DiscordBotManager(command_prefix='!', intents=intents)

    bot_task = asyncio.create_task(bot.start_bot(BOT_TOKEN))
    trigger_task = asyncio.create_task(trigger_send_message(bot))

    try:
        await asyncio.gather(bot_task, trigger_task)
    except KeyboardInterrupt:
        await bot.close_bot()


if __name__ == "__main__":
    asyncio.run(main())