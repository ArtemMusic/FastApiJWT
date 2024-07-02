import uuid
from datetime import timedelta, datetime
import bcrypt
import jwt
from core.config import settings


def encode_jwt(
        payload: dict,
        private_key: str = settings.auth_jwt.private_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm,
        expire_minutes: int = settings.auth_jwt.access_token_exp_min,
        expire_timedelta: timedelta | None = None
) -> str:
    to_encode_payload = payload.copy()
    now = datetime.utcnow()

    if expire_timedelta:
        exp = now + expire_timedelta
    else:
        exp = now + timedelta(minutes=expire_minutes)

    to_encode_payload.update(
        iat=now,
        exp=exp,
        jti=str(uuid.uuid4()),
    )

    return jwt.encode(to_encode_payload, private_key, algorithm=algorithm)


def decode_jwt(
        token: str | bytes,
        public_key: str = settings.auth_jwt.public_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm,
) -> str:
    return jwt.decode(token, public_key, algorithms=[algorithm])


def hash_password(
        password: str
) -> bytes:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def check_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password=password.encode(), hashed_password=hashed_password)
