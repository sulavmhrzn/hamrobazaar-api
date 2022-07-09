import contextlib
import typing

import aiohttp


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
        """Return session object"""
        if not self.session:
            self.session = aiohttp.ClientSession()
        return self.session
