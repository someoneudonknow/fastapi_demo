from http import HTTPStatus
from typing import Generic, TypeVar

from pydantic.generics import GenericModel

T = TypeVar("T")


class SuccessResponse(GenericModel, Generic[T]):
    message: str
    status: int
    metadata: T

    def __init__(self, message=None, status_code=None, metadata=None, **kwargs):
        super().__init__(
            message=message or HTTPStatus.OK.phrase,
            status=status_code or HTTPStatus.OK,
            metadata=metadata or {},
        )


class Created(SuccessResponse[T]):
    def __init__(self, message=None, metadata: T = None, **kwargs):
        super().__init__(
            message=message or HTTPStatus.CREATED.phrase,
            status_code=HTTPStatus.CREATED,
            metadata=metadata,
        )


class NotModified(SuccessResponse[T]):
    def __init__(self, message=None, metadata: T = None, **kwargs):
        super().__init__(
            message=message or HTTPStatus.NOT_MODIFIED.phrase,
            status_code=HTTPStatus.NOT_MODIFIED,
            metadata=metadata,
        )
