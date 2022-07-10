from dataclasses import dataclass


@dataclass
class Category:
    id: str
    name: str
    slug: str
    child_cat: list["ChildCategory"]


@dataclass
class ChildCategory:
    cat_id: str
    parent_cat_id: str
    name: str
    slug: str


@dataclass
class Product:
    id: str
    name: str
    description: str
    price: int
    category_name: str
    created_on: str
    expiry_date: str
    location: str
