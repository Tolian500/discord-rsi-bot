import os
import discord
import asyncio
import time
from discord_bot_manager import DiscordBotManager
import bybit_manager
import logging


# Secrets
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Parameters for the Bybit API
symbol = "SOLUSDT"
interval = "60"  # Use "60" for 1-hour interval

# Parameters for the Discord bot
RISING_EMOJI = "\U0001F534"
LOWERING_EMOJI = "\U0001F7E2"

# Define global interval variables
TEST_INTERVAL = 5  # Interval in seconds for testing purposes
PRODUCTION_INTERVAL = 3600  # Interval in seconds for production (1 hour)

async def main():
    # Initialize Discord bot
    intents = discord.Intents.all()
    bot = DiscordBotManager(command_prefix='!', intents=intents, channel_id=DISCORD_CHANNEL_ID)

    # Start the Discord bot
    bot_task = asyncio.create_task(bot.start_bot(BOT_TOKEN))

    try:
        await asyncio.gather(bot_task, trigger_send_message(bot))  # Pass bot object to trigger_send_message
    except KeyboardInterrupt:
        await bot.close_bot()

async def trigger_send_message(bot):
    # Initialize BybitManager with API credentials
    manager = bybit_manager.BybitManager(API_KEY, API_SECRET)

    while True:
        # Calculate start_time and end_time for fetching K-line data
        start_time = int((time.time() - 60 * 60 * 24) * 1000)  # 24 hours ago in milliseconds
        end_time = int(time.time() * 1000)  # current time in milliseconds

        # Fetch spot K-line data for SOL/USDT
        kline_data = manager.fetch_kline_data(symbol, interval, start_time, end_time)

        if kline_data:
            # Calculate RSI
            df = manager.calculate_rsi(kline_data)

            # Find first non-NaN RSI value and its timestamp
            first_valid_rsi = df['RSI'].dropna().iloc[0]
            first_valid_time = df.index[df['RSI'].notna()].tolist()[0]

            # test
            first_valid_rsi = 72
            # Initialize send_message flag
            send_message = False

            # Check RSI condition and format message with emojis
            if first_valid_rsi <= 30 or first_valid_rsi >= 70:
                send_message = True
                if first_valid_rsi <= 30:
                    emoji = RISING_EMOJI  # Red circle emoji for low RSI
                elif first_valid_rsi >= 70:
                    emoji = LOWERING_EMOJI  # Green circle emoji for high RSI
            else:
                emoji = ""

            # Format the message with appropriate emoji
            rsi_message = f"{emoji} RSI: {first_valid_rsi:.2f} at {first_valid_time.strftime('%Y-%m-%d %H:%M:%S')}"

            # Send message to Discord
            if send_message:
                await bot.send_time_message(rsi_message)
                logger.info(f"RSI conditions met. RSI: {first_valid_rsi:.2f}")
                logger.info(f"Message sent: {rsi_message}")
            else:
                logger.info(f"RSI conditions didn't meet. RSI: {first_valid_rsi:.2f}")
                logger.info("Message not sent")

        await asyncio.sleep(TEST_INTERVAL)

if __name__ == "__main__":
    asyncio.run(main())
