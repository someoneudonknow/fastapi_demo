import jwt
from fastapi import Depends, Header, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.configs.config import settings
from app.cores.error_response import ForbiddenException
from app.services.token_service import verify_token

auth_scheme = HTTPBearer()


async def get_current_user(
    request: Request,
    authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
    refresh_token: str = Header(None, description="Refresh token (optional)"),
):
    if not refresh_token:
        try:
            decoded_authorization = verify_token(
                authorization.credentials, settings.access_secret
            )

            request.state.user = decoded_authorization

            return {"user": decoded_authorization}
        except Exception:
            raise ForbiddenException("Access denied")

    else:
        try:
            decoded_refresh_token = verify_token(refresh_token, settings.refresh_secret)

            request.state.user = decoded_refresh_token
            request.state.refresh_token = refresh_token

            return {"user": decoded_refresh_token, "refresh_token": refresh_token}
        except Exception:
            raise ForbiddenException("Access denied")
