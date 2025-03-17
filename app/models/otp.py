from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

from app.databases.init_postgresql import Base
from app.models.user import USER_TABLE_NAME

TOKEN_TABLE_NAME = "otps"


class OTP(Base):
    __tablename__ = TOKEN_TABLE_NAME

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )
    user_id = Column(Integer, ForeignKey(f"{USER_TABLE_NAME}.id"), nullable=False)
    otp = Column(String, nullable=False)
    expired_at = Column(DateTime, nullable=False)
