# 1) Ensure uv is on PATH
export PATH="$HOME/.local/bin:$PATH"

# 2) Change into your project directory
cd /home/jana/Documents/CollectorDiscord/knowledgecollector || exit 1

# 3) Run the fetcher (50 = number of messages to pull each time)
uv run -m src.discord.main 50 >> discord_fetch.log 2>&1
