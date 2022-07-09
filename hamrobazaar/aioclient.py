import contextlib
import typing

import aiohttp
from aiohttp.typedefs import JSONEncoder


class HamrobazaarClient(contextlib.AbstractAsyncContextManager):
    def __init__(self, api_key: str, session: aiohttp.ClientSession = None):
        self.api_key = api_key
        self.session = session

    async def __aexit__(
        self,
        exception_type: typing.Type[Exception],
        exception: Exception,
        exception_traceback,
    ) -> None:
        await self.close()

    async def close(self) -> None:
        """Close opened session"""
        if self.session:
            await self.session.close()

    def _get_session(self) -> aiohttp.ClientSession:
        """Return or create a session

        Returns:
            aiohttp.ClientSession
        """
        if not self.session:
            self.session = aiohttp.ClientSession()
        return self.session

    def _make_headers(self, **kwargs) -> dict:
        """Construct headers with api_key and extra kwargs

        Returns:
            dict: constructed headers
        """

        headers = {k: str(v) for k, v in kwargs.items()}
        headers["ApiKey"] = self.api_key
        return headers

    async def _make_request(
        self, method: str, url: str, json: typing.Optional[JSONEncoder] = None
    ) -> dict:
        """Makes a request to the url

        Args:
            method (str): HTTP method to use
            url (str): URL to make request to
            json (typing.Optional[JSONEncoder], optional): Json body to send during request. Defaults to None.

        Returns:
            dict: decoded json response
        """
        session = self._get_session()
        headers = self._make_headers()

        async with session.request(method, url, headers=headers, json=json) as response:
            try:
                return await response.json()
            except aiohttp.ClientResponseError as e:
                # Todo: Log messages
                response.raise_for_status()
