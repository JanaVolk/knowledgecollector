import httpx
from .config import DISCORD_TOKEN, CHANNEL_ID

API_URL = f"https://discord.com/api/v10/channels/{CHANNEL_ID}/messages"

async def fetch_messages(limit: int = 10) -> list[dict]:
    """
    Return the last `limit` messages from the configured channel.
    """
    headers = {"Authorization": f"Bot {DISCORD_TOKEN}"}
    params  = {"limit": limit}
    async with httpx.AsyncClient() as client:
        resp = await client.get(API_URL, headers=headers, params=params)
        resp.raise_for_status()
        return resp.json()
