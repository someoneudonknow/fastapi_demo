import json
from datetime import datetime, timedelta

import jwt

from app.services.redis_service import RedisService
from app.utils.redis_util import create_redis_key

ENCODE_ALGORITHM = "RS256"
USER_TOKEN_PREFIX = "user_tokens"


class TokenService:
    @staticmethod
    def verify_token(token: str, public_key: str):
        return jwt.decode(token, public_key, algorithms=[ENCODE_ALGORITHM])

    @staticmethod
    def create_token_pair(payload: dict, public_key: str, private_key: str):
        access_token_expiration_date = datetime.now() + timedelta(days=2)
        refresh_token_expiration_date = datetime.now() + timedelta(days=7)

        access_token_payload = payload | {"exp": access_token_expiration_date}
        refresh_token_payload = payload | {"exp": refresh_token_expiration_date}

        access_token = jwt.encode(
            access_token_payload,
            private_key,
            algorithm=ENCODE_ALGORITHM,
            headers={"alg": ENCODE_ALGORITHM, "typ": "JWT"},
        )
        refresh_token = jwt.encode(
            refresh_token_payload,
            private_key,
            algorithm=ENCODE_ALGORITHM,
            headers={"alg": ENCODE_ALGORITHM, "typ": "JWT"},
        )

        try:
            decoded = jwt.decode(
                access_token, public_key, algorithms=[ENCODE_ALGORITHM]
            )
            print("Token successfully verified:", decoded)
        except jwt.ExpiredSignatureError:
            print("Token expired")
        except jwt.InvalidTokenError as err:
            print("Invalid token", err)

        return {"accessToken": access_token, "refreshToken": refresh_token}

    @staticmethod
    def delete_token(id: int):
        key = create_redis_key(USER_TOKEN_PREFIX, id)
        return RedisService.delete(key)

    @staticmethod
    def get_token(id: int):
        key = create_redis_key(USER_TOKEN_PREFIX, id)
        data = RedisService.get(key)

        return json.loads(data) if data is not None else None

    @staticmethod
    def insert_token(
        user_id: int,
        public_key: str,
        refresh_token: str,
        private_key: str,
        refresh_tokens_used: list[str] = [],
    ):
        key = create_redis_key(USER_TOKEN_PREFIX, user_id)
        payload = {
            "private_key": private_key,
            "public_key": public_key,
            "refresh_token": refresh_token,
            "refresh_tokens_used": refresh_tokens_used,
        }

        return RedisService.set(key, json.dumps(payload))
