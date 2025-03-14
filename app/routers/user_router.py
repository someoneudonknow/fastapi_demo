from fastapi import APIRouter, Depends

from app.controllers.user_controller import UserController
from app.cores.success_response import SuccessResponse
from app.dependencies.auth_dependency import get_current_user
from app.dependencies.require_roles import require_role
from app.models.user import UserRole
from app.schemas.paginate import PaginateResponse
from app.schemas.user import UserResponse, UserUpdate

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.get("/me", response_model=SuccessResponse[UserResponse])
def get_user(current_user=Depends(get_current_user)):
    return UserController.get_user(current_user["user"]["user_id"])


@user_router.patch("/me", response_model=SuccessResponse[UserUpdate])
def update_user(current_user=Depends(get_current_user), update_body: UserUpdate = None):
    return UserController.update_user(current_user["user"]["user_id"], update_body)


@user_router.get("", response_model=SuccessResponse[PaginateResponse[UserResponse]])
def get_all(_=Depends(require_role(UserRole.ADMIN)), page: int = 1, limit: int = 10):
    return UserController.get_users(page, limit)


@user_router.delete("/{user_id}", response_model=SuccessResponse[int])
def delete_user(
    current_user=Depends(require_role(UserRole.ADMIN)), user_id: int | None = None
):
    print(user_id, current_user)
    return UserController.delete_user(user_id, current_user)
