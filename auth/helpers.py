from datetime import timedelta
from api_v1.users.schemas import User
from auth import utils
from core.config import settings

TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"


def create_jwt(
        token_type: str,
        token_data: dict,
        expire_minutes: int = settings.auth_jwt.access_token_exp_min,
        expire_timedelta: timedelta | None = None
) -> str:
    jwt_payload = {TOKEN_TYPE_FIELD: token_type}
    jwt_payload.update(token_data)
    return utils.encode_jwt(payload=jwt_payload, expire_minutes=expire_minutes, expire_timedelta=expire_timedelta)


def create_access_token(user: User) -> str:
    jwt_payload = {
        'sub': user.id,
        'username': user.username,
        'email': user.email,
    }

    return create_jwt(token_type=ACCESS_TOKEN_TYPE, token_data=jwt_payload,
                      expire_minutes=settings.auth_jwt.access_token_exp_min)


def create_refresh_token(user: User) -> str:
    jwt_payload = {
        'sub': user.id,
    }

    return create_jwt(token_type=REFRESH_TOKEN_TYPE, token_data=jwt_payload,
                      expire_timedelta=timedelta(days=settings.auth_jwt.refresh_token_expire_days))
