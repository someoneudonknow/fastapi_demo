import json
from datetime import datetime, timedelta

import jwt

from app.configs.config import settings
from app.databases.init_postgresql import get_db
from app.models.token import Token

ENCODE_ALGORITHM = "HS256"
USER_TOKEN_PREFIX = "user_tokens"


def verify_token(token: str, public_key: str):
    return jwt.decode(token, public_key, algorithms=[ENCODE_ALGORITHM])


def create_token_pair(payload: dict, old_refresh_token: str | None = None):
    access_token_expiration_date = datetime.now() + timedelta(minutes=1)
    refresh_token_expiration_date = datetime.now() + timedelta(days=30)

    if old_refresh_token:
        try:
            decoded_old_refresh_token = jwt.decode(
                old_refresh_token,
                settings.refresh_secret,
                algorithms=[ENCODE_ALGORITHM],
            )
            refresh_token_expiration_date = datetime.fromtimestamp(
                decoded_old_refresh_token["exp"]
            )
        except jwt.ExpiredSignatureError:
            print(
                "Old refresh token expired, generating a new one with 7-day expiration."
            )
        except jwt.InvalidTokenError:
            print(
                "Invalid old refresh token, generating a new one with 7-day expiration."
            )

    access_token_payload = payload | {"exp": access_token_expiration_date}
    refresh_token_payload = payload | {"exp": refresh_token_expiration_date}

    access_token = jwt.encode(
        access_token_payload,
        settings.access_secret,
        algorithm=ENCODE_ALGORITHM,
        headers={"alg": ENCODE_ALGORITHM, "typ": "JWT"},
    )
    refresh_token = jwt.encode(
        refresh_token_payload,
        settings.refresh_secret,
        algorithm=ENCODE_ALGORITHM,
        headers={"alg": ENCODE_ALGORITHM, "typ": "JWT"},
    )

    return {"accessToken": access_token, "refreshToken": refresh_token}


def delete_token(user_id: int):
    db = get_db()
    token = db.query(Token).filter(Token.user_id == user_id).first()

    if not token:
        return 0

    db.delete(token)
    db.commit()

    return 1


def get_token_by_user_id(id: int):
    db = get_db()
    return db.query(Token).filter(Token.user_id == id).first()


def insert_or_update_token(
    user_id: int, refresh_token: str, refresh_tokens_used: list[str] = []
):
    db = get_db()
    found_token = db.query(Token).filter(Token.user_id == user_id).first()

    if found_token is None:
        token = Token(
            user_id=user_id,
            refresh_token=refresh_token,
            refresh_tokens_used=refresh_tokens_used,
        )

        db.add(token)
        db.commit()
        db.refresh(token)

        return token

    found_token.refresh_token = refresh_token
    found_token.refresh_tokens_used = refresh_tokens_used

    db.commit()
    db.refresh(found_token)

    return found_token
