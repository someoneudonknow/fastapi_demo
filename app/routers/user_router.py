from fastapi import APIRouter, Depends, Request

from app.cores.success_response import SuccessResponse
from app.dependencies.auth_dependency import get_current_user
from app.dependencies.require_roles import require_role
from app.models.user import UserRole
from app.schemas.paginate import PaginateResponse
from app.schemas.user import UserResponse, UserUpdate
from app.services.user_service import get_user, get_users, soft_delete_user, update_user

user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.get(
    "/me",
    response_model=SuccessResponse[UserResponse],
    dependencies=[Depends(get_current_user)],
)
def get_me(request: Request):
    return SuccessResponse(metadata=get_user(request.state.user["user_id"]))


@user_router.patch(
    "/me",
    response_model=SuccessResponse[UserUpdate],
    dependencies=[Depends(get_current_user)],
)
def update_me(request: Request, update_body: UserUpdate = None):
    return SuccessResponse(
        metadata=update_user(request.state.user["user_id"], update_body)
    )


@user_router.get(
    "/{user_id}",
    response_model=SuccessResponse[UserResponse],
    dependencies=[Depends(require_role(UserRole.ADMIN))],
)
def get_user_by_id(user_id: int | None = None):
    return SuccessResponse(metadata=get_user(user_id))


@user_router.get(
    "",
    response_model=SuccessResponse[PaginateResponse[UserResponse]],
    dependencies=[Depends(require_role(UserRole.ADMIN))],
)
def get_all_users(page: int = 1, limit: int = 10, query: str = ""):
    return SuccessResponse(metadata=get_users(page, limit, query))


@user_router.delete(
    "/{user_id}",
    response_model=SuccessResponse[int],
    dependencies=[Depends(require_role(UserRole.ADMIN))],
)
def delete_user_by_id(request: Request, user_id: int | None = None):
    return SuccessResponse(metadata=soft_delete_user(user_id, request.state.user))
