import contextlib
import typing

import aiohttp
from aiohttp.typedefs import JSONEncoder
from slugify import slugify

from .exceptions import CategoryNotFound, ProductNotFound, ReachedLastPage
from .types import Category, ChildCategory, Product, ProductDetail, SortBy
from .utils import GET_ALL_CATEGORY_URL, MAIN_PAGE_URL, SEARCH_URL, format_product


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

    async def main_page_products(
        self, page_number: int = 1, page_size: int = 10
    ) -> list[Product]:
        """Return products displayed on main page

        Args:
            page_number (int, optional): Page number to show products of. Defaults to 1.
            page_size (int, optional): Number of products to display. Defaults to 10.

        Returns:
            list[Product]
        """
        url = f"{MAIN_PAGE_URL}?pageNumber={page_number}&pageSize={page_size}"

        response = await self._make_request("get", url)
        data = response["data"]

        return [format_product(product) for product in data]

    async def _get_products(
        self, category: Category, page_number: int = 1, page_size: int = 10
    ) -> list[Product]:
        category_id = category.id
        url = f"{MAIN_PAGE_URL}?categoryId={category_id}pageNumber={page_number}&pageSize={page_size}"

        response = await self._make_request("get", url)
        total_pages = response["totalPages"]

        if page_number > total_pages:
            raise ReachedLastPage(
                f"You have reached the last page. {page_number} exceeds {total_pages}"
            )

        data = response["data"]

        return [format_product(product) for product in data]

    async def get_products(
        self, category: Category, page_number: int = 1, page_size: int = 10
    ) -> list[Category]:
        """Return products based on given category

        Args:
            category (Category): Category to return products from
            page_number (int, optional): Page number to return products from. Defaults to 1.
            page_size (int, optional): Number of products to display. Defaults to 10.

        Raises:
            ReachedLastPage: If reached last page.

        Returns:
            list[Category]
        """
        return await self._get_products(category, page_number, page_size)

    async def _search_products(
        self,
        name: str,
        page_number: int = 1,
        page_size: int = 10,
        price_from: int = 0,
        price_to: int = 0,
        is_price_negotiable: None | bool = None,
        sort_by: SortBy = SortBy.A_TO_Z,
        is_hb_select: bool = False,
    ):
        body = {
            "pageNumber": page_number,
            "pageSize": page_size,
            "latitude": "0",
            "longitude": "0",
            "searchParams": {"searchValue": name, "SortBy": ""},
            "filterParams": {
                "condition": 0,
                "priceFrom": price_from,
                "priceTo": price_to,
                "isPriceNegotiable": is_price_negotiable,
                "category": "",
                "categoryIds": "eb9c8147-07c0-4951-a962-381cdb400e37",
                "brandIds": "",
                "brand": "",
            },
            "sortParam": sort_by.value,
            "isHBSelect": is_hb_select,
            "deviceId": "e62ffe29-194a-4fd6-a606-486ab0a604f0",
            "deviceSource": "web",
        }
        response = await self._make_request("post", url=SEARCH_URL, json=body)
        data = response["data"]
        return [format_product(product) for product in data]

    async def search_products(
        self,
        name: str,
        page_number: int = 1,
        page_size: int = 10,
        price_from: int = 0,
        price_to: int = 0,
        is_price_negotiable: None | bool = None,
        sort_by: SortBy = SortBy.A_TO_Z,
        is_hb_select: bool = False,
    ):
        return await self._search_products(
            name,
            page_number,
            page_size,
            price_from,
            price_to,
            is_price_negotiable,
            sort_by,
            is_hb_select,
        )

    async def _get_product_detail(self, product_id: str) -> ProductDetail:
        url = f"{MAIN_PAGE_URL}/{product_id}"

        response = await self._make_request("get", url)
        errors = response.get("errors", None)
        
        if errors:
            raise ProductNotFound("Product with that id was not found.")

        if response["status"]["message"][0] == "Product not found!":
            raise ProductNotFound("Product with that id was not found.")

        product = response["data"]
        specs_list = []

        for specs in product["productAttributeValues"]:
            specs_list.append({specs["attributeName"]: specs["value"]})

        return format_product(product, specs_list)

    async def get_product_detail(self, product_id: str) -> ProductDetail:
        """Return product detail for a specific product id

        Args:
            product_id (str): Product id to get details for

        Raises:
            ProductNotFound: When no product with given id is found

        Returns:
            ProductDetail
        """
        return await self._get_product_detail(product_id)
