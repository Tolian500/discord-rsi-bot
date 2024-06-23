# RSI Discord Bot 🤖

This project is an RSI (Relative Strength Index) Discord bot that sends notifications to a specified Discord channel when certain RSI conditions are met. The bot is built using Python and runs inside a Docker container.

## Features

- 📈 Connects to the Bybit API to fetch RSI data for a specified symbol and interval.
- ✉️ Sends notifications to a Discord channel when RSI conditions are met.
- ⏱️ Calculates and includes the **delay** between fetching data and RSI calculation in notifications. (2-4 seconds)
- ⚙️ Can be configured using environment variables.

## Prerequisites

- Docker
- Discord bot token
- Bybit API key and secret

## Functional Requirements

1. **Fetch Spot K-line Data**
   - K-line data for the SOL/USDT pair is fetched from Bybit using the Unified Trading HTTP API.
   - The `fetch_kline_data` method in `BybitManager` class retrieves K-line data based on specified symbol, interval, start time, and end time.

2. **Calculate RSI (Relative Strength Index)**
   - RSI is calculated using the closing prices from the fetched K-line data.
   - The `calculate_rsi` method in `BybitManager` class computes RSI using the `ta.momentum.RSIIndicator` from the `ta` library with a window of 14 periods.

## How RSI Calculation Works

- **Step-by-step RSI Calculation Process:**
  1. **Data Preparation**: The fetched K-line data is transformed into a Pandas DataFrame.
  2. **Timestamp Handling**: Timestamps are converted to datetime objects for readability and indexing.
  3. **RSI Calculation**: The RSI is computed using the closing prices column (`df['close']`) with a window size of 14 periods.
  4. **Integration**: The RSI values are integrated back into the DataFrame (`df['RSI']`).

## Setup

1. **Clone the repository**

    ```bash
    git clone https://github.com/Tolian500/discord-rsi-bot.git
    cd rsi-discord-bot
    ```

2. **Create a `.env` file** in the project directory and add the following variables:

    ```env
    BOT_TOKEN=<your_discord_bot_token>
    API_KEY=<your_bybit_api_key>
    API_SECRET=<your_bybit_api_secret>
    DISCORD_CHANNEL_ID=<your_discord_channel_id>
    ```

3. **Build the Docker image**

    ```bash
    docker build -t rsi-discord-bot:beta .
    ```

4. **Run the Docker container**

    ```bash
    docker run --env-file .env -d --name rsi-discord-bot rsi-discord-bot:beta
    ```

    To override the `DISCORD_CHANNEL_ID` at runtime, use the following command:

    ```bash
    docker run --env-file .env -e DISCORD_CHANNEL_ID=1254421075094409270 -d --name rsi-discord-bot-new rsi-discord-bot:beta
    ```

5. **Stopping and removing the container**

    If you need to stop and remove the container:

    ```bash
    docker stop rsi-discord-bot
    docker rm rsi-discord-bot
    ```

6. **Running a new container with a different name**

    ```bash
    docker run --env-file .env -d --name rsi-discord-bot-new rsi-discord-bot:beta
    ```

## Files

- **main.py**: The main script that runs the bot and connects to the Bybit API.
- **discord_bot_manager.py**: Contains the `DiscordBotManager` class which manages the Discord bot functionality.
- **Dockerfile**: The Dockerfile used to create the Docker image for the bot.
- **.env**: Environment variables file (not included in the repository, needs to be created).

## Important Notes

- Ensure your `.env` file is not included in version control to keep your secrets safe.
- Replace placeholder values in the `.env` file with your actual credentials and IDs.

## Delay Feature

- The bot now calculates and includes the delay between the real-time UTC and the time when the RSI calculation was performed in milliseconds. This delay is included in the notification messages sent to the Discord channel, providing insight into the timing of data processing.

## Common Issues

- If you encounter an error related to the Discord bot token being `None`, ensure that your `.env` file is correctly formatted and the `BOT_TOKEN` variable is set.

## License

This project is licensed under the MIT License.
