from discord.ext import commands
import os
import datetime

class DiscordBotManager(commands.Bot):
    def __init__(self, channel_id: int, **kwargs):
        super().__init__(**kwargs)
        self.channel_id = channel_id

    async def send_time_message(self, message=""):
        utc_now = datetime.datetime.utcnow()
        current_utc_time = utc_now.strftime("%H:%M:%S UTC")
        channel = self.get_channel(self.channel_id)
        if channel:
            await channel.send(f'{message} - Current UTC time: {current_utc_time}')
            print(f'Sent message at {current_utc_time}')
        else:
            print(f'Channel with ID {self.channel_id} not found.')

    async def on_ready(self):
        print(f'{self.user.name} has connected to Discord!')

    async def start_bot(self, token):
        await self.start(token)

    async def close_bot(self):
        await self.close()
