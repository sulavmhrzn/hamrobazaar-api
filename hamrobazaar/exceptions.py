class HamrobazaarException(Exception):
    """Base exception class for hamrobazaar api"""


class CategoryNotFound(HamrobazaarException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
