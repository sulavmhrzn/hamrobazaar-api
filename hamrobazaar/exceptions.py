class HamrobazaarException(Exception):
    """Base exception class for hamrobazaar api"""


class CategoryNotFound(HamrobazaarException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class ReachedLastPage(HamrobazaarException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class ProductNotFound(HamrobazaarException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
