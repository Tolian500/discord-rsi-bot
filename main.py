import os
import discord
import asyncio
import time
import logging
from discord_bot_manager import DiscordBotManager
import bybit_manager
from datetime import datetime, timedelta, timezone
import pytz

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

async def main():
    # Initialize Discord bot
    intents = discord.Intents.all()
    bot = DiscordBotManager(command_prefix='!', intents=intents, channel_id=DISCORD_CHANNEL_ID)

    # Start the Discord bot
    bot_task = asyncio.create_task(bot.start_bot(BOT_TOKEN))

    try:
        await asyncio.gather(bot_task, minute_task(bot))  # Pass bot object to minute_task
    except KeyboardInterrupt:
        await bot.close_bot()

async def minute_task(bot):
    while True:
        await trigger_send_message(bot)
        # Calculate the time until the next full minute in UTC
        now = datetime.now(timezone.utc)
        next_minute = (now + timedelta(minutes=60)).replace(second=0, microsecond=0)
        delta = (next_minute - now).total_seconds()

        # Wait until the next full minute
        await asyncio.sleep(delta)

async def trigger_send_message(bot):
    # Initialize BybitManager with API credentials
    manager = bybit_manager.BybitManager(API_KEY, API_SECRET)

    # Fetch current UTC time
    utc_now = datetime.now(timezone.utc)

    # Convert UTC time to desired format
    current_utc_time = utc_now.strftime("%Y-%m-%d %H:%M:%S UTC")

    # Calculate start_time and end_time for fetching K-line data
    start_time = int((time.time() - 60 * 60 * 24) * 1000)  # 24 hours ago in milliseconds
    end_time = int(time.time() * 1000)  # current time in milliseconds

    # Record the current time before fetching data
    before_fetch = time.time()

    # Fetch spot K-line data for SOL/USDT
    kline_data = manager.fetch_kline_data(symbol, interval, start_time, end_time)

    # Record the time after fetching data
    after_fetch = time.time()

    # Calculate the delay in milliseconds
    delay_ms = int((after_fetch - before_fetch) * 1000)

    if kline_data:
        # Calculate RSI
        df = manager.calculate_rsi(kline_data)

        # Find first non-NaN RSI value and its timestamp
        first_valid_rsi = df['RSI'].dropna().iloc[0]
        first_valid_time = df.index[df['RSI'].notna()].tolist()[0]

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

        # Format the message with appropriate emoji and delay
        rsi_message = f"{emoji} RSI for {symbol}: {first_valid_rsi:.2f} at {first_valid_time.strftime('%Y-%m-%d %H:%M:%S')} " \
                      f"(UTC Time: {current_utc_time}, Delay: {delay_ms} ms)"

        # Send message to Discord
        if send_message:
            await bot.send_time_message(rsi_message)
            logger.info(f"RSI conditions met. RSI: {first_valid_rsi:.2f}")
            logger.info(f"Message sent: {rsi_message}")
        else:
            logger.info(f"RSI conditions didn't meet. RSI: {first_valid_rsi:.2f}")
            logger.info("Message not sent")

if __name__ == "__main__":
    asyncio.run(main())
