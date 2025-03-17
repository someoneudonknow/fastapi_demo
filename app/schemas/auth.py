from pydantic import BaseModel, EmailStr, Field

from app.schemas.user import UserResponse


class TokensResponse(BaseModel):
    accessToken: str = Field(examples=["example_access_token"])
    refreshToken: str = Field(examples=["example_refresh_token"])


class Register(BaseModel):
    password: str = Field(examples=["supersecretpassword"])
    name: str = Field(examples=["Hatsune Miku"])
    email: EmailStr = Field(examples=["hatsune.miku@gmail.com"])


class Login(BaseModel):
    email: EmailStr = Field(examples=["hatsune.miku@gmail.com"])
    password: str = Field(examples=["supersecretpassword"])


class AuthResponse(BaseModel):
    tokens: TokensResponse


class ForgotPassword(BaseModel):
    email: EmailStr = Field(examples=["hatsune.miku@gmail.com"])


class ResetPassword(BaseModel):
    email: EmailStr = Field(examples=["hatsune.miku@gmail.com"])
    new_password: str = Field(examples=["supersecretpassword"])
    otp: str = Field(examples=["12kskjaldjlajdlajsklj"])
