from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    password: str = Field(examples=["supersecretpassword"])
    name: str = Field(examples=["Hatsune Miku"])
    email: str = Field(examples=["hatsune.miku@gmail.com"])


class UserResponse(BaseModel):
    id: int = Field(examples=[1])
    email: str = Field(examples=["hatsune.miku@gmail.com"])
    name: str = Field(examples=["Hatsune Miku"])
    role: str = Field(examples=["user"])
    created_at: datetime = Field(examples=["2022-01-01T00:00"])
    updated_at: datetime = Field(examples=["2022-01-01T00:00"])

    class Config:
        from_attributes = True
        json_encoder: {datetime: lambda v: v.isoformat()}


class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, examples=["Hatsune Miku"])
