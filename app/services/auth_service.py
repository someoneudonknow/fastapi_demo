from app.configs.config import settings
from app.cores.error_response import (
    BadRequestException,
    ConflictException,
    ForbiddenException,
    InternalServerException,
    NotFoundException,
    UnauthorizedException,
)
from app.databases.init_postgresql import get_db
from app.models.user import User, UserRole
from app.schemas.auth import Login, Register
from app.services.mail_service import send_email
from app.services.otp_service import generate_otp, insert_otp, verify_otp
from app.services.security_service import check_hash, generate_salt, hash
from app.services.token_service import (
    create_token_pair,
    delete_token,
    get_token_by_user_id,
    insert_or_update_token,
)
from app.services.user_service import create_user, get_user_by_email
from app.templates.templates import verify_email_template
from app.utils.email_utils import replace_template_data


async def forgot_password(email: str):
    user = get_user_by_email(email)

    if not user:
        raise NotFoundException("User not found")

    token = generate_otp()

    inserted_otp = insert_otp(user.id, token)

    if not inserted_otp:
        raise InternalServerException(
            "Something went wrong while creating your profile, please try again later"
        )

    link = f"{settings.backend_url}/verify-email/{inserted_otp.otp}"
    expired_minutes = settings.otp_expriration_in_minutes

    html = replace_template_data(
        verify_email_template(),
        {"expiredMinutes": expired_minutes, "verifyLink": link, "rawToken": token},
    )

    await send_email("Verify your email", html, [user.email])

    return 1


def reset_password(email: str, new_password: str, otp: str):
    db = get_db()
    found_user = db.query(User).filter(User.email == email).first()

    if not found_user:
        raise NotFoundException("User not found")

    if not verify_otp(found_user.id, otp):
        raise UnauthorizedException("OTP is invalid")

    hashed_password = hash(new_password, generate_salt())

    found_user.password = hashed_password

    db.commit()
    db.refresh(found_user)

    return 1


def login(body: Login):
    user = get_user_by_email(body.email)

    if not user:
        raise NotFoundException("You're not registered")

    is_pass_correct = check_hash(body.password, user.password)

    if not is_pass_correct:
        raise UnauthorizedException("Authentication failed")

    payload = {"user_id": user.id, "email": user.email, "role": user.role}
    tokens = create_token_pair(payload)

    if not tokens:
        raise InternalServerException(
            "Something went wrong while creating your profile, please try again later"
        )

    inserted_token = insert_or_update_token(user.id, tokens["refreshToken"], [])

    if not inserted_token:
        raise InternalServerException(
            "Something went wrong while creating your profile, please try again later"
        )

    return tokens


def register(payload: Register):
    user = get_user_by_email(payload.email)

    if user:
        raise ConflictException("You're already registered")

    salt = generate_salt()
    hashed_password = hash(payload.password, salt)
    new_user = create_user(
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
    tokens = create_token_pair(payload)

    if not tokens:
        raise InternalServerException(
            "Something went wrong while creating your profile, please try again later"
        )

    inserted_token = insert_or_update_token(new_user.id, tokens["refreshToken"], [])

    if not inserted_token:
        raise InternalServerException(
            "Something went wrong while creating your profile, please try again later"
        )

    return tokens


def logout(user_id: int):
    delete_token(user_id)
    return 1


def refreshAToken(user, refresh_token):
    if refresh_token is None:
        raise BadRequestException("Refresh token not found")

    found_token = get_token_by_user_id(user["user_id"])

    if found_token is None:
        raise BadRequestException("You're not logged in")

    tokens_used = found_token.refresh_tokens_used

    if refresh_token in tokens_used:
        delete_token(user["user_id"])

        raise ForbiddenException(
            "There're some suspicious behavior of your account! please log in again"
        )

    if refresh_token != found_token.refresh_token:
        raise ForbiddenException("Refresh token is invalid")

    payload = {
        "user_id": user["user_id"],
        "email": user["email"],
        "role": user["role"],
    }

    tokens = create_token_pair(payload)

    updated_token = found_token.__dict__

    updated_token["refresh_tokens_used"].append(refresh_token)
    updated_token["refresh_token"] = tokens["refreshToken"]

    inserted_token = insert_or_update_token(
        user["user_id"],
        updated_token["refresh_token"],
        updated_token["refresh_tokens_used"],
    )

    if inserted_token is None:
        raise InternalServerException(
            "Something went wrong while creating your profile, please try again later"
        )

    return tokens
