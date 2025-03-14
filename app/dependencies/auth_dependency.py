import jwt
from fastapi import Header

from app.cores.error_response import BadRequestException, ForbiddenException
from app.services.token_service import TokenService

AUTHORIZATION = "authorization"
REFRESH_TOKEN = "refresh-token"
CLIENT_ID = "x-client-id"


async def get_current_user(
    x_client_id: str = Header(..., description="Client ID for authentication"),
    x_authorization: str = Header(..., description="Bearer token for authentication"),
    refresh_token: str = Header(None, description="Refresh token (optional)"),
):
    if not x_client_id:
        raise BadRequestException("Invalid request")

    if not x_authorization:
        raise BadRequestException("Invalid request")

    tokens = TokenService.get_token(x_client_id)

    if tokens is None:
        raise BadRequestException("You're not logged in")

    if not refresh_token:
        try:
            decoded_authorization = TokenService.verify_token(
                x_authorization, tokens["public_key"]
            )

            return {"user": decoded_authorization}
        except Exception:
            raise ForbiddenException("Token is invalid")
    else:
        try:
            decoded_refresh_token = TokenService.verify_token(
                refresh_token, tokens["public_key"]
            )

            return {"user": decoded_refresh_token, "refresh_token": refresh_token}
        except Exception:
            raise ForbiddenException("Token is invalid")
