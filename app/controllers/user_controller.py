from app.cores.success_response import SuccessResponse
from app.schemas.user import UserUpdate
from app.services.user_service import UserService


class UserController:
    @staticmethod
    def get_user(user_id: int):
        return SuccessResponse(metadata=UserService.get_user(user_id))

    @staticmethod
    def update_user(id: int, updateBody: UserUpdate):
        return SuccessResponse(metadata=UserService.update_user(id, updateBody))

    @staticmethod
    def get_users(page: int = 1, limit: int = 10):
        return SuccessResponse(metadata=UserService.get_users(page, limit))

    @staticmethod
    def delete_user(user_id: int, current_user: dict):
        return SuccessResponse(metadata=UserService.delete_user(user_id, current_user))
