from typing import Annotated

from fastapi import APIRouter, Depends, Request

from app.cores.success_response import Created, SuccessResponse
from app.dependencies.auth_dependency import get_current_user
from app.schemas.auth import (
    ForgotPassword,
    Login,
    Register,
    ResetPassword,
    TokensResponse,
)
from app.services.auth_service import (
    forgot_password,
    login,
    logout,
    refreshAToken,
    register,
    reset_password,
)

auth_router = APIRouter(prefix="/auths", tags=["Authentication"])


@auth_router.post("/reset-password", response_model=SuccessResponse[int])
def on_reset_password(payload: ResetPassword):
    return SuccessResponse(
        metadata=reset_password(payload.email, payload.new_password, payload.otp)
    )


@auth_router.post("/forgot-password", response_model=SuccessResponse[int])
async def on_forgot_password(payload: ForgotPassword):
    return SuccessResponse(
        message="Email has been sent", metadata=await forgot_password(payload.email)
    )


@auth_router.post("/register", response_model=SuccessResponse[TokensResponse])
def on_register(payload: Register):
    return SuccessResponse(metadata=register(payload))


@auth_router.post("/login", response_model=SuccessResponse[TokensResponse])
def on_login(payload: Login):
    return SuccessResponse(metadata=login(payload))


@auth_router.post(
    "/logout",
    response_model=SuccessResponse[int],
    dependencies=[Depends(get_current_user)],
)
def on_logout(request: Request):
    return SuccessResponse(metadata=logout(request.state.user["user_id"]))


@auth_router.post(
    "/refresh",
    response_model=SuccessResponse[TokensResponse],
    # response_model=SuccessResponse[dict],
    dependencies=[Depends(get_current_user)],
)
def on_refresh(request: Request):
    return SuccessResponse(
        metadata=refreshAToken(request.state.user, request.state.refresh_token)
    )
