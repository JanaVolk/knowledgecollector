# KnowledgeCollector Discord

A minimal Python application that fetches messages and attachments from a specified Discord channel and writes them into timestamped JSON files for downstream ingestion into the Smart KMS collector pipeline.

---

## Project Structure

```plaintext
knowledgecollector-discord/
├── .env.example              # Example environment variables
├── fetch_discord.sh          # Shell wrapper for cron jobs
├── discord_fetch.log         # Log of fetch script runs
├── Dockerfile                # Optional Docker build
├── pyproject.toml            # Project dependencies and metadata
├── README.md                 # This documentation
└── src/
    └── discord/
        ├── __init__.py       # Package initializer (can be empty)
        ├── config.py         # Loads DISCORD_BOT_TOKEN & DISCORD_CHANNEL_ID
        ├── discord_api.py    # HTTP client to fetch Discord messages
        └── main.py           # Fetch & write JSON once
```  

---

## Prerequisites

- **Python 3.13+** with the `uv` toolchain installed (e.g. `pipx install uv`).  
- A **Discord Bot** configured in the Developer Portal with:
  - **Message Content Intent** enabled  
  - **Read Message History** permission  
- **cron** (on Linux/macOS) for scheduling periodic fetches.

---

## Creating or Using the Discord Bot

You have two options for the bot:

1. **Use our hosted bot** (no need to register your own):
   - Simply invite the existing bot using the **Invite Link** below.
   - Request the `DISCORD_BOT_TOKEN` and `DISCORD_CHANNEL_ID` from the Smart KMS team and populate your `.env` file.

2. **Create your own bot** (if you prefer full control):
   1. **Open Discord Developer Portal**  
      Go to https://discord.com/developers/applications and click **New Application**. Give it a name (e.g. `KnowledgeCollectorBot`).
   2. **Add a Bot user**  
      In the sidebar, select **Bot**, then click **Add Bot** → **Yes, do it**.
   3. **Enable Privileged Intents**  
      Under **Privileged Gateway Intents**, enable **Message Content Intent** so the bot can read message text.
   4. **Copy the Bot Token**  
      Click **Reset Token** (if needed) and then **Copy**. Place this value into your `.env` as `DISCORD_BOT_TOKEN`.
   5. **Invite to your server**  
      - In **OAuth2 → URL Generator**, check the **bot** scope.  
      - Under **Bot Permissions**, select at least **View Channels** and **Read Message History**.  
      - Copy the generated URL, paste it into your browser, select your server, and authorize the bot.
   6. **Obtain Channel ID**  
      In Discord, enable **Developer Mode** (User Settings → Advanced). Right‑click your target channel, select **Copy ID**, and use this value as `DISCORD_CHANNEL_ID` in your `.env`.

---

## Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USER/knowledgecollector-discord.git
   cd knowledgecollector-discord
   ```

2. **Copy and populate environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your values:
   # DISCORD_BOT_TOKEN=your_bot_token_here
   # DISCORD_CHANNEL_ID=123456789012345678
   ```

3. **Install dependencies**
   ```bash
   uv sync
   ```
   This creates a private venv and installs all dependencies from `pyproject.toml` (`fastapi`, `httpx`, `python-dotenv`, etc.).

4. **Test fetching once**
   ```bash
   uv run -m src.discord.main 20
   ```
   - Fetches the last 20 messages and prints them.  
   - Writes a file named `<epoch_ms>.json` in the project root.

---

## Running the Discord Collector

To run the bot script that fetches messages and writes JSON files without exposing an HTTP endpoint:

```bash
# Run your collector (default: 50 messages)
uv run -m src.discord.main

# Or specify a custom limit, e.g. last 20 messages
uv run -m src.discord.main 20
```

Each invocation creates a timestamped `<epoch_ms>.json` file in the project root.  

## Docker (Optional) (Optional)

1. **Build the image**
   ```bash
   docker build -t knowledgecollector-discord .
   ```
2. **Run the container**
   ```bash
   docker run -p 8000:8000 knowledgecollector-discord
   ```
3. **Access logs and files**
   - JSON files and logs are stored in the container’s working directory 
   - Mount a host volume if you need persistence

---

## Scheduling with cron

1. **Make the wrapper executable**
   ```bash
   chmod +x fetch_discord.sh
   ```

2. **Open crontab**
   ```bash
   crontab -e
   ```

3. **Add your cron job** (e.g., every 15 minutes)
   ```cron
   */15 * * * * /path to repository/fetch_discord.sh
   ```
   - Adjust the path to match your local setup.  

4. **Verify your job**
   ```bash
   crontab -l
   tail -n 20 discord_fetch.log
   ls -1t *.json | head
   ```

---

## Customization

- **Fetch limit**: Change the argument in `fetch_discord.sh` or pass a different number to `uv run -m src.discord.main <limit>`.
- **Output directory**: Modify the write path in `src/discord/main.py` if you prefer a custom folder.

---

## Troubleshooting

- **No JSON files**: Check `.env` values, bot permissions, and logs in `discord_fetch.log`.
- **Import errors**: Ensure you run with `uv run -m src.discord.main` from the project root.
- **Cron not firing**: Confirm `crontab -l` shows your entry, inspect `/var/log/syslog` for cron errors, and verify script paths.

---
