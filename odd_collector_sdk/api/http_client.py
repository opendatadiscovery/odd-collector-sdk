from typing import Any

from aiohttp import ClientSession, ClientTimeout


class HttpClient:
    def __init__(self, token: str, connection_timeout_seconds: int = 300) -> None:
        self.headers = {
            "content-type": "application/json",
            "Authorization": f"Bearer {token}",
        }
        self.timeout = ClientTimeout(total=connection_timeout_seconds)

    async def post(self, url: str, data: Any, session: ClientSession, **kwargs):
        return await session.post(url=url, data=data, headers=self.headers, **kwargs)
