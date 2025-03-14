from app.cores.success_response import Created, SuccessResponse
from app.schemas.auth import Login, Register
from app.services.auth_service import AuthService

auth_service = AuthService()


class AuthController:
    @staticmethod
    def register(payload: Register):
        return Created(metadata=AuthService.register(payload))

    @staticmethod
    def login(payload: Login):
        return SuccessResponse(metadata=AuthService.login(payload))

    @staticmethod
    def logout(id: int):
        return SuccessResponse(metadata=AuthService.logout(id))

    @staticmethod
    def refresh(user, refresh_token):
        return SuccessResponse(metadata=AuthService.refreshAToken(user, refresh_token))
