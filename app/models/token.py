from sqlalchemy import ARRAY, Column, ForeignKey, Integer, String

from app.databases.init_postgresql import Base
from app.models.user import USER_TABLE_NAME

TOKEN_TABLE_NAME = "tokens"


class Token(Base):
    __tablename__ = TOKEN_TABLE_NAME

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )
    user_id = Column(Integer, ForeignKey(f"{USER_TABLE_NAME}.id"), nullable=True)
    refresh_token = Column(String, nullable=False)
    refresh_tokens_used = Column(ARRAY(String), default=dict)
