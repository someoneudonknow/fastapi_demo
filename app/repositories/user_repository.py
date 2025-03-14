from fastapi import Depends
from sqlalchemy.orm import Session

from app.cores.error_response import NotFoundException
from app.databases.init_postgresql import get_db
from app.models.user import User, UserRole
from app.schemas.user import UserUpdate


class UserRepository:
    @staticmethod
    def update_role_by_id(id: int, role: UserRole):
        db = get_db()
        user = db.query(User).filter(User.id == id).first()

        if not user:
            return None

        user.role = role

        db.commit()
        db.refresh(user)

        return user

    @staticmethod
    def delete_by_id(user_id: int):
        db = get_db()
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            raise NotFoundException("User not found")

        db.delete(user)
        db.commit()
        return 1

    @staticmethod
    def get_all(page: int = 1, limit: int = 10):
        db = get_db()
        skip = limit * (page - 1)
        return db.query(User).offset(skip).limit(limit).all()

    @staticmethod
    def count_all():
        db = get_db()
        return db.query(User).count()

    @staticmethod
    def get_one(user_id: int):
        db = get_db()
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_one_by_email(email: str):
        db = get_db()
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def update_by_id(id: int, update_body: UserUpdate):
        db = get_db()
        user = db.query(User).filter(User.id == id).first()

        print(user)

        if not user:
            return None

        update_data = update_body.dict(exclude_unset=True, exclude_none=True)

        for key, value in update_data.items():
            setattr(user, key, value)

        db.commit()
        db.refresh(user)

        return user

    @staticmethod
    def create(email: str, name: str, password: str, role: UserRole):
        db = get_db()

        user = User(
            email=email,
            name=name,
            password=password,
            role=role,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user
