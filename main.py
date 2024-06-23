import discord
import os
import asyncio
import time
from discord_bot_manager import DiscordBotManager
import bybit_manager

# Parameters for the Bybit API
API_KEY = os.environ["bybit-api-key"]
API_SECRET = os.environ["bybit-api-secret"]
symbol = "SOLUSDT"
interval = "60"  # Use "60" for 1-hour interval

# Parameters for the Discord bot
BOT_TOKEN = os.environ["discord-bot-token"]
LOWERING_EMOJI = "\U0001F534"
RISING_EMOJI = "\U0001F7E2"


async def main():
    # Initialize BybitManager with API credentials
    manager = bybit_manager.BybitManager(API_KEY, API_SECRET)

    # Calculate start_time and end_time for fetching K-line data
    start_time = int((time.time() - 60 * 60 * 24) * 1000)  # 24 hours ago in milliseconds
    end_time = int(time.time() * 1000)  # current time in milliseconds

    # Fetch spot K-line data for SOL/USDT
    kline_data = manager.fetch_kline_data(symbol, interval, start_time, end_time)

    if kline_data:
        # Calculate RSI
        df = manager.calculate_rsi(kline_data)
        print("DataFrame with RSI:")
        print(df)

        # Print example K-line data
        manager.print_kline_data(kline_data, symbol)

        # Find first non-NaN RSI value and its timestamp
        first_valid_rsi = df['RSI'].dropna().iloc[0]
        first_valid_time = df.index[df['RSI'].notna()].tolist()[0]

        # Check RSI condition and format message with emojis
        if first_valid_rsi <= 30:
            emoji = LOWERING_EMOJI  # 🔴 emoji for low RSI
        elif first_valid_rsi >= 70:
            emoji = RISING_EMOJI  # 🟢 emoji for high RSI
        else:
            emoji = ""

        # Format the message with appropriate emoji
        rsi_message = f"{emoji} RSI: {first_valid_rsi:.2f} at {first_valid_time.strftime('%Y-%m-%d %H:%M:%S')}"

        # Initialize Discord bot
        intents = discord.Intents.all()
        bot = DiscordBotManager(command_prefix='!', intents=intents)

        # Define bot task and message sending task
        bot_task = asyncio.create_task(bot.start_bot(BOT_TOKEN))
        message_task = asyncio.create_task(trigger_send_message(bot, rsi_message))

        try:
            await asyncio.gather(bot_task, message_task)
        except KeyboardInterrupt:
            await bot.close_bot()


async def trigger_send_message(bot, message=""):
    while True:
        await bot.send_time_message(message)
        await asyncio.sleep(5)


if __name__ == "__main__":
    asyncio.run(main())
