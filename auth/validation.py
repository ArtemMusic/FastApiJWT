from fastapi import HTTPException, status, Form, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from api_v1.users.schemas import User
from auth.helpers import TOKEN_TYPE_FIELD
from auth import utils
from jwt.exceptions import InvalidTokenError
from db import UserORM
from db.depends import session_depends

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')


async def validate_auth_user(session: AsyncSession = session_depends, username=Form(), password=Form()) -> UserORM:
    unauthed_usr = HTTPException(status.HTTP_401_UNAUTHORIZED, detail='invalid username or password')
    stmt = select(UserORM).where(UserORM.username == username)
    result: Result = await session.execute(stmt)
    user = result.scalar()

    if not user:
        raise unauthed_usr
    if not (utils.check_password(password, user.password)):
        raise unauthed_usr

    return user


def get_auth_user_from_token_of_type(token_type: str):
    async def get_auth_user_from_token(
            payload: dict = Depends(get_current_token_payload),
            session: AsyncSession = session_depends
    ) -> User:
        validate_token_type(payload, token_type)
        return await get_user_by_token_sub(payload, session)

    return get_auth_user_from_token


def get_current_token_payload(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = utils.decode_jwt(token=token)
    except InvalidTokenError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'invalid token error: {e}')

    return payload


def validate_token_type(payload: dict, token_type: str) -> bool:
    current_token_type = payload.get(TOKEN_TYPE_FIELD)

    if current_token_type == token_type:
        return True

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"invalid token type {current_token_type!r} expected {token_type!r}",
    )


async def get_user_by_token_sub(payload: dict, session: AsyncSession) -> User:
    sub: str | None = payload.get("sub")

    if sub:
        stmt = select(UserORM).where(UserORM.id == sub)
        result: Result = await session.execute(stmt)
        user = result.scalar()
        return user

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid (user not found)",
    )
