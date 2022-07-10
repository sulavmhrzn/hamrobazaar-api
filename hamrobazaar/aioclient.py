import contextlib
import typing

import aiohttp
from aiohttp.typedefs import JSONEncoder
from slugify import slugify

from .exceptions import CategoryNotFound
from .types import Category, ChildCategory
from .utils import GET_ALL_CATEGORY_URL


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

    async def _get_categories(self) -> list[Category]:
        response = await self._make_request("get", GET_ALL_CATEGORY_URL)
        data = response["data"]
        result = []
        child_cats = []

        for parent in data:
            for child in parent["categories"]:
                child_cats.append(
                    ChildCategory(
                        parent_cat_id=parent["id"],
                        cat_id=child["id"],
                        name=child["name"],
                        slug=slugify(child["name"]),
                    )
                )
            result.append(
                Category(
                    id=parent["id"],
                    name=parent["name"],
                    slug=slugify(parent["name"]),
                    child_cat=child_cats,
                )
            )
            # set child_cats to empty list with every iteration
            # so that every category gets its own child category
            child_cats = []
        return result

    async def get_categories(self) -> list[Category]:
        """Return all categories present in hamrobazaar

        Returns:
            list[Category]
        """
        return await self._get_categories()

    async def _filter_category(self, name: str) -> Category:
        categories = await self.get_categories()
        for category in categories:
            if name.lower() == category.name.lower():
                return category
        raise CategoryNotFound("Category not found.")

    async def filter_category(self, name: str) -> Category:
        """Filter category with name

        Args:
            name (str): Name of the category

        Raises:
            CategoryNotFound: If category with that name was not found

        Returns:
            Category
        """
        return await self._filter_category(name)
