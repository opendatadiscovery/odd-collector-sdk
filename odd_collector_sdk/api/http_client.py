from typing import Any

from aiohttp import ClientSession, ClientTimeout

from odd_collector_sdk.errors import PlatformApiError


class HttpClient:
    def __init__(self, token: str, connection_timeout_seconds: int = 300) -> None:
        self.headers = {
            "content-type": "application/json",
            "Authorization": f"Bearer {token}",
        }
        self.timeout = ClientTimeout(total=connection_timeout_seconds)

    async def post(self, url: str, data: Any, **kwargs):
        async with ClientSession() as session:
            response = await session.post(
                url=url, data=data, headers=self.headers, **kwargs
            )
            if response.status >= 400:
                body = await response.json()

                raise PlatformApiError(body)
            return response
