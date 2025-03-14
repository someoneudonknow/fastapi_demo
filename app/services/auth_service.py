from app.cores.error_response import (
    BadRequestException,
    ConflictException,
    ForbiddenException,
    InternalServerException,
    NotFoundException,
    UnauthorizedException,
)
from app.models.user import UserRole
from app.schemas.auth import Login, Register
from app.schemas.user import UserCreate
from app.services.security_service import SecurityService
from app.services.token_service import TokenService
from app.services.user_service import UserService
from app.utils.sqlalchemy_util import to_dict


class AuthService:
    @staticmethod
    def login(body: Login):
        user = UserService.get_user_by_email(body.email)

        if not user:
            raise NotFoundException("You're not registered")

        is_pass_correct = SecurityService.check_hash(body.password, user.password)

        if not is_pass_correct:
            raise UnauthorizedException("Authentication failed")

        payload = {"user_id": user.id, "email": user.email, "role": user.role}
        private_key, public_key = SecurityService.generate_key_pair()

        if not private_key or not public_key:
            raise InternalServerException(
                "Something went wrong while creating your profile, please try again later"
            )

        tokens = TokenService.create_token_pair(payload, public_key, private_key)

        if not tokens:
            raise InternalServerException(
                "Something went wrong while creating your profile, please try again later"
            )

        inserted_token = TokenService.insert_token(
            user.id, public_key, tokens["refreshToken"], private_key
        )

        if not inserted_token:
            raise InternalServerException(
                "Something went wrong while creating your profile, please try again later"
            )

        return {"user": to_dict(user, excludes=["password"]), "tokens": tokens}

    @staticmethod
    def register(payload: Register):
        user = UserService.get_user_by_email(payload.email)

        if user:
            raise ConflictException("You're already registered")

        salt = SecurityService.generate_salt()
        hashed_password = SecurityService.hash(payload.password, salt)
        new_user = UserService.create_user(
            name=payload.name,
            password=hashed_password,
            email=payload.email,
            role=UserRole.USER,
        )

        if not new_user:
            raise InternalServerException(
                "Something went wrong while creating your profile, please try again later"
            )

        payload = {
            "user_id": new_user.id,
            "email": new_user.email,
            "role": new_user.role,
        }
        private_key, public_key = SecurityService.generate_key_pair()

        if not private_key or not public_key:
            raise InternalServerException(
                "Something went wrong while creating your profile, please try again later"
            )

        tokens = TokenService.create_token_pair(payload, public_key, private_key)

        if not tokens:
            raise InternalServerException(
                "Something went wrong while creating your profile, please try again later"
            )

        inserted_token = TokenService.insert_token(
            new_user.id, public_key, tokens["refreshToken"], private_key
        )

        if not inserted_token:
            raise InternalServerException(
                "Something went wrong while creating your profile, please try again later"
            )

        return {"user": to_dict(new_user, excludes=["password"]), "tokens": tokens}

    @staticmethod
    def logout(user_id: int):
        TokenService.delete_token(user_id)
        return 1

    @staticmethod
    def refreshAToken(user, refresh_token):
        if refresh_token is None:
            raise BadRequestException("Refresh token not found")

        found_token = TokenService.get_token(user["user_id"])

        if found_token is None:
            raise BadRequestException("You're not logged in")

        tokens_used = found_token["refresh_tokens_used"]

        if refresh_token in tokens_used:
            TokenService.delete_token(user["user_id"])

            raise ForbiddenException(
                "There're some suspicious behavior of your account! please log in again"
            )

        if refresh_token != found_token["refresh_token"]:
            raise ForbiddenException("Refresh token is invalid")

        payload = {
            "user_id": user["user_id"],
            "email": user["email"],
            "role": user["role"],
        }

        tokens = TokenService.create_token_pair(
            payload, found_token["public_key"], found_token["private_key"]
        )

        updated_token = found_token

        updated_token["refresh_tokens_used"].append(refresh_token)
        updated_token["refresh_token"] = tokens["refreshToken"]

        inserted_token = TokenService.insert_token(
            user["user_id"],
            updated_token["public_key"],
            updated_token["refresh_token"],
            updated_token["private_key"],
            updated_token["refresh_tokens_used"],
        )

        if inserted_token is None:
            raise InternalServerException(
                "Something went wrong while creating your profile, please try again later"
            )

        return tokens
