import asyncio
import json
from datetime import datetime
from .discord_api import fetch_messages
from .config import CHANNEL_ID

async def main(limit: int = 50):
    # 1) pull raw Discord messages
    raw = await fetch_messages(limit=limit)

    # 2) normalize each message
    normalized = []
    for m in raw:
        normalized.append({
            "createdDateTime": m["timestamp"],              # ISO timestamp from Discord
            "user": {
                "id": m["author"]["id"],                    # bot sees author.id
                "displayName": m["author"]["username"]      # and username
            },
            "body": m.get("content", "")                   # message text
        })

    # 3) build the top-level wrapper
    now = datetime.utcnow()
    ts_iso = now.isoformat(timespec="milliseconds") + "Z"
    epoch_ms = str(int(now.timestamp() * 1000))

    payload = {
        "typefield": "messages",
        "platform":  "discord",
        "id":         epoch_ms,
        "timestamp":  ts_iso,
        "content": {
            "channelId": CHANNEL_ID,   # numeric string from your .env
            "messages":  normalized
        }
    }

    # 4) write to JSON file
    filename = f"{epoch_ms}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print(f"Wrote {len(normalized)} messages to {filename}")

if __name__ == "__main__":
    # you can pass an argument like `python -m src.discord.main 20`
    import sys
    lim = int(sys.argv[1]) if len(sys.argv) > 1 else 50
    asyncio.run(main(limit=lim))
