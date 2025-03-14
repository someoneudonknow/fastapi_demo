from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.configs.config import settings

DATABASE_URL = f"postgresql://{settings.db_user}:{settings.db_pass}@{settings.db_host}/{settings.db_name}"

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)

Base = declarative_base()


def generate_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_db():
    generator = generate_session()
    return next(generator)


def init_db():
    Base.metadata.create_all(bind=engine)

    from app.configs.config import settings
    from app.models.user import UserRole
    from app.services.security_service import SecurityService
    from app.services.user_service import UserService

    admin_email = settings.admin_email
    admin_name = settings.admin_name
    admin_password = settings.admin_password

    admin = UserService.get_user_by_email(admin_email)

    if admin is None:
        password_hashed = SecurityService.hash(
            admin_password, SecurityService.generate_salt()
        )

        UserService.create_user(
            email=admin_email,
            name=admin_name,
            password=password_hashed,
            role=UserRole.ADMIN,
        )
