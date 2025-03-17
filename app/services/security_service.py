import bcrypt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa


def generate_salt() -> bytes:
    return bcrypt.gensalt()


def hash(text: str, salt: bytes) -> str:
    return bcrypt.hashpw(text.encode(), salt).decode()


def check_hash(text: str, hash: str) -> bool:
    return bcrypt.checkpw(text.encode(), hash.encode())


def generate_key_pair(key_size=4096, public_exponent=65537) -> tuple[str, str]:
    private_key = rsa.generate_private_key(
        public_exponent=public_exponent,
        key_size=key_size,
    )

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    public_key = private_key.public_key()

    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    return private_pem.decode(), public_pem.decode()
