from datetime import datetime
from typing import List
from fastapi import HTTPException, status
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from api_v1.users.schemas import UserIn, UserOut, User
from auth.utils import hash_password
from db import UserORM


async def get_user_by_id(user_id: int, session: AsyncSession, is_formated: bool = False) -> User | UserORM | None:
    stmt = select(UserORM).where(UserORM.id == user_id)
    result: Result = await session.execute(stmt)
    user: UserORM = result.scalar()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with id "{user_id}" not found'
        )

    if is_formated:
        return User(
            id=user.id,
            username=user.username,
            email=user.email,
            created_at=user.created_at
        )
    else:
        return user


async def check_email(user: UserIn, session: AsyncSession) -> UserORM:
    result: Result = await session.execute(select(UserORM).where(UserORM.email == user.email))
    existing_user: UserORM = result.scalar()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'Email "{user.email}" already exists.'
        )

    return existing_user


async def create_product(user: UserIn, session: AsyncSession) -> UserOut:
    await check_email(user, session)

    data = user.model_dump()
    user = UserORM(**data)
    user.password = hash_password(user.password)
    user.created_at = datetime.utcnow()
    session.add(user)

    user = UserOut(
        username=user.username,
        email=user.email,
        created_at=user.created_at
    )

    await session.commit()
    return user


async def get_all_users(session: AsyncSession) -> List[User] | None:
    stmt = select(UserORM).order_by(UserORM.id.desc())
    result: Result = await session.execute(stmt)
    users: List[UserORM] = list(result.scalars())

    users_out = []
    for user in users:
        users_out.append(
            User(
                id=user.id,
                username=user.username,
                email=user.email,
                created_at=user.created_at
            )
        )

    return users_out


async def delete_user(user_id: int, session: AsyncSession) -> User:
    user: UserORM = await get_user_by_id(user_id, session)

    if user is not None:
        await session.delete(user)
        await session.commit()

        return User(
            id=user.id,
            username=user.username,
            email=user.email,
            created_at=user.created_at
        )
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found")


async def update_user(updated_user: UserIn, user_id: int, session: AsyncSession) -> User:
    user: User = await get_user_by_id(user_id, session)

    if user is not None:
        old_updated_user = updated_user

        updated_user = updated_user.model_dump()

        if updated_user.get('email') != user.email:
            await check_email(old_updated_user, session)

        new_password = hash_password(updated_user.get('password'))
        updated_user.pop('password')
        updated_user.update(password=new_password)

        for key, value in updated_user.items():
            setattr(user, key, value)

        user = User(
            id=user.id,
            username=user.username,
            email=user.email,
            created_at=user.created_at
        )

        await session.commit()
        return user
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id "{user_id}" not found')
