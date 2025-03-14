from fastapi import APIRouter, Depends

from app.controllers.auth_controller import AuthController
from app.cores.success_response import Created, SuccessResponse
from app.dependencies.auth_dependency import get_current_user
from app.schemas.auth import AuthResponse, Login, Register, TokensResponse

auth_router = APIRouter(prefix="/auths", tags=["Authentication"])


@auth_router.post("/register", response_model=Created[AuthResponse])
def register(body: Register):
    return AuthController.register(body)


@auth_router.post("/login", response_model=SuccessResponse[AuthResponse])
def login(body: Login):
    return AuthController.login(body)


@auth_router.post("/logout", response_model=SuccessResponse[int])
def logout(current_user=Depends(get_current_user)):
    return AuthController.logout(current_user["user"]["user_id"])


@auth_router.post("/refresh", response_model=SuccessResponse[TokensResponse])
def refresh(current_user=Depends(get_current_user)):
    return AuthController.refresh(current_user["user"], current_user["refresh_token"])
