from typing import Generic, TypeVar

from pydantic.generics import GenericModel

T = TypeVar("T")


class PaginateResponse(GenericModel, Generic[T]):
    list: list[T]
    totalPages: int
    page: int
    limit: int
