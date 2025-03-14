from http import HTTPStatus


class ErrorResponse(Exception):
    def __init__(self, message, status_code):
        self.status_code = status_code
        self.message = message


class InternalServerException(ErrorResponse):
    def __init__(self, message=HTTPStatus.INTERNAL_SERVER_ERROR.phrase):
        super().__init__(message, HTTPStatus.INTERNAL_SERVER_ERROR)


class ConflictException(ErrorResponse):
    def __init__(self, message=HTTPStatus.CONFLICT.phrase):
        super().__init__(message, HTTPStatus.CONFLICT)


class NotFoundException(ErrorResponse):
    def __init__(self, message=HTTPStatus.NOT_FOUND.phrase):
        super().__init__(message, HTTPStatus.NOT_FOUND)


class UnauthorizedException(ErrorResponse):
    def __init__(self, message=HTTPStatus.UNAUTHORIZED.phrase):
        super().__init__(message, HTTPStatus.UNAUTHORIZED)


class BadRequestException(ErrorResponse):
    def __init__(self, message=HTTPStatus.BAD_REQUEST.phrase):
        super().__init__(message, HTTPStatus.BAD_REQUEST)


class ForbiddenException(ErrorResponse):
    def __init__(self, message=HTTPStatus.FORBIDDEN.phrase):
        super().__init__(message, HTTPStatus.FORBIDDEN)
