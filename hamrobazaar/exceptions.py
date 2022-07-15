class HamrobazaarException(Exception):
    """Base exception class for hamrobazaar api"""


class CategoryNotFound(HamrobazaarException):
    """Raised when category with given filter is not found"""

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class ReachedLastPage(HamrobazaarException):
    """Raised when given page numbers exceeds last page"""

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class ProductNotFound(HamrobazaarException):
    """Raised when product with given filter is not found."""

    def __init__(self, *args: object) -> None:
        super().__init__(*args)
