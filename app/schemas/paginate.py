from typing import Generic, TypeVar

from pydantic.generics import GenericModel

T = TypeVar("T")


class PaginateResponse(GenericModel, Generic[T]):
    list: list[T]
    total: int
    page: int
