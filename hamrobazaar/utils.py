from .types import Product, ProductDetail

API_BASE_URL = "https://api.hamrobazaar.com/api"
GET_ALL_CATEGORY_URL = f"{API_BASE_URL}/AppData/GetAllCategory"
MAIN_PAGE_URL = f"{API_BASE_URL}/Product"
SEARCH_URL = f"{API_BASE_URL}/Search/Products"


def format_product(product: dict, specs: list[dict] = None) -> Product:
    if specs:
        return ProductDetail(
            id=product["id"],
            name=product["name"],
            description=product["description"],
            price=product["price"],
            category_name=product["categoryName"],
            created_on=product["createdOn"],
            expiry_date=product["expiryDate"],
            location=product["location"]["locationDescription"],
            specifications=specs,
        )
    return Product(
        id=product["id"],
        name=product["name"],
        description=product["description"],
        price=product["price"],
        category_name=product["categoryName"],
        created_on=product["createdOn"],
        expiry_date=product["expiryDate"],
        location=product["location"]["locationDescription"],
    )
