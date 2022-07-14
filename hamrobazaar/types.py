from dataclasses import dataclass
from enum import Enum


@dataclass
class Category:
    """Represents a category"""
    id: str
    name: str
    slug: str
    child_cat: list["ChildCategory"]


@dataclass
class ChildCategory:
    """Represents a child category inside Category"""
    cat_id: str
    parent_cat_id: str
    name: str
    slug: str


@dataclass
class Product:
    """Represent a product"""
    id: str
    name: str
    description: str
    price: int
    category_name: str
    created_on: str
    expiry_date: str
    location: str


@dataclass
class ProductDetail(Product):
    """Represent a product with extra attributes"""
    specifications: list[dict]


class SortBy(Enum):
    """Sort crieteria for sort param"""
    A_TO_Z = 1
    Z_TO_A = 2
    LOW_TO_HIGH = 3
    HIGH_TO_LOW = 4
    RECENT = 5
    OLDER = 6
