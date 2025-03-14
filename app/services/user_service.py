from app.cores.error_response import BadRequestException
from app.models.user import UserRole
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserUpdate
from app.utils.debug import logger
from app.utils.sqlalchemy_util import to_dict


class UserService:
    @staticmethod
    def get_user(user_id: int):
        return UserRepository.get_one(user_id)

    @staticmethod
    def get_user_by_email(email: str):
        return UserRepository.get_one_by_email(email)

    @staticmethod
    def update_user(id: int, update_body: UserUpdate):
        return to_dict(
            UserRepository.update_by_id(id, update_body), excludes=["password"]
        )

    @staticmethod
    def update_user_role(id: int, role: UserRole):
        return UserRepository.update_role_by_id(id, role)

    @staticmethod
    def create_user(email: str, name: str, password: str, role: str):
        return UserRepository.create(email, name, password, role)

    @staticmethod
    def get_users(page: int = 1, limit: int = 10):
        return {
            "list": [
                to_dict(u, excludes=["password"])
                for u in UserRepository.get_all(page, limit)
            ],
            "page": page,
            "total": UserRepository.count_all(),
        }

    @staticmethod
    def delete_user(user_id: int, current_user: dict):
        if user_id == current_user["user"]["user_id"]:
            raise BadRequestException("You can't delete your own account bruh")

        return UserRepository.delete_by_id(user_id)
