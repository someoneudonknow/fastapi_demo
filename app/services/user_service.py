import math

from sqlalchemy import func

from app.cores.error_response import BadRequestException, NotFoundException
from app.databases.init_postgresql import get_db
from app.models.user import User, UserRole
from app.schemas.user import UserUpdate
from app.utils.sqlalchemy_util import to_dict


def get_user(user_id: int):
    db = get_db()
    found_user = db.query(User).filter(User.id == user_id).first()

    if found_user is None:
        raise NotFoundException("User not found")

    return found_user


def get_user_by_email(email: str):
    db = get_db()

    return db.query(User).filter(User.is_deleted == False, User.email == email).first()


def update_by_id(id: int, update_body: UserUpdate):
    db = get_db()
    user = db.query(User).filter(User.id == id).first()

    if not user:
        return None

    update_data = update_body.dict(exclude_unset=True, exclude_none=True)

    for key, value in update_data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)

    return user


def update_user(id: int, update_body: UserUpdate):
    return to_dict(update_by_id(id, update_body), excludes=["password"])


def update_user_role(id: int, role: UserRole):
    db = get_db()
    user = db.query(User).filter(User.id == id).first()

    if not user:
        return None

    user.role = role

    db.commit()
    db.refresh(user)

    return user


def create_user(email: str, name: str, password: str, role: str):
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


def get_users(page: int = 1, limit: int = 10, query: str = ""):
    data, count = find_and_count(limit, page, query)
    return {
        "list": data,
        "page": page,
        "totalPages": int(math.ceil(count / limit)),
        "limit": limit,
    }


def find_and_count(limit: int = 10, page: int = 1, query: str = ""):
    selected_fields = [User.id, User.email, User.name, User.role, User.is_deleted]
    db = get_db()

    query = query.lower()

    db_query = db.query(*selected_fields).filter(
        # User.is_deleted == False,
        func.lower(User.name).contains(query)
        | func.lower(User.email).contains(query),
    )

    count = db_query.count()
    data = db_query.offset(limit * (page - 1)).limit(limit).all()

    return data, count


def soft_delete_user(user_id: int, current_user: dict):
    if user_id == current_user["user_id"]:
        raise BadRequestException("You can't delete your own account bruh")

    db = get_db()

    found_user = db.query(User).filter(User.id == user_id).first()

    found_user.is_deleted = True

    db.commit()
    db.refresh(found_user)

    return 1


def delete_user(user_id: int, current_user: dict):
    if user_id == current_user["user_id"]:
        raise BadRequestException("You can't delete your own account bruh")

    db = get_db()
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise NotFoundException("User not found")

    db.delete(user)
    db.commit()
    return 1
