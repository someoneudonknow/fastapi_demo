import secrets
from datetime import datetime, timedelta

from app.cores.error_response import NotFoundException, UnauthorizedException
from app.databases.init_postgresql import get_db
from app.models.otp import OTP
from app.services.security_service import check_hash, generate_salt, hash


def generate_otp():
    return secrets.token_urlsafe(16)


def insert_otp(user_id: int, otp: str):
    db = get_db()

    expired_at = datetime.utcnow() + timedelta(minutes=5)
    found_otp = db.query(OTP).filter(OTP.user_id == user_id).first()

    if found_otp:
        db.delete(found_otp)
        db.commit()

    hashed_otp = hash(otp, generate_salt())

    otp = OTP(user_id=user_id, otp=hashed_otp, expired_at=expired_at)
    db.add(otp)
    db.commit()
    db.refresh(otp)

    return otp


def verify_otp(user_id: int, otp: str):
    db = get_db()
    found_otp = db.query(OTP).filter(OTP.user_id == user_id).first()

    if not found_otp:
        return False

    if not check_hash(otp, found_otp.otp):
        return False

    if found_otp.expired_at < datetime.utcnow():
        return False

    db.delete(found_otp)
    db.commit()

    return True
