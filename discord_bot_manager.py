import discord
from discord.ext import commands
import os
import datetime

class DiscordBotManager(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.channel_id = int(os.environ["discord-testchannel-id"])

    async def send_time_message(self):
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        channel = self.get_channel(self.channel_id)
        if channel:
            await channel.send(f'Current server time is: {current_time}')
            print(f'Sent message at {current_time}')
        else:
            print(f'Channel with ID {self.channel_id} not found.')

    async def on_ready(self):
        print(f'{self.user.name} has connected to Discord!')

    async def start_bot(self, token):
        await self.start(token)

    async def close_bot(self):
        await self.close()
