from typing import List

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

from app.configs.config import settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.mail_username,
    MAIL_PASSWORD=settings.mail_password,
    MAIL_FROM=settings.mail_username,
    MAIL_PORT=settings.mail_port,
    MAIL_SERVER=settings.mail_server,
    MAIL_STARTTLS=settings.mail_starttls,
    MAIL_SSL_TLS=settings.mail_ssl_tls,
    USE_CREDENTIALS=settings.use_credentials,
    VALIDATE_CERTS=settings.validate_certs,
)


async def send_email(subject: str, body: str, recipients: List[str]):
    fm = FastMail(conf)

    message = MessageSchema(
        subject=subject, recipients=recipients, body=body, subtype=MessageType.html
    )

    await fm.send_message(message)
