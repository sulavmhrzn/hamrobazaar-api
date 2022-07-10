from dataclasses import dataclass
from enum import Enum


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


class SortBy(Enum):
    A_TO_Z = 1
    Z_TO_A = 2
    LOW_TO_HIGH = 3
    HIGH_TO_LOW = 4
    RECENT = 5
    OLDER = 6
