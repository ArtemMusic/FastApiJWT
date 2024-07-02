from typing import List

from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.users import crud
from api_v1.users.schemas import UserIn, UserOut, User
from db.depends import session_depends

router = APIRouter(
    prefix='/user', tags=['User CRUD']
)


@router.post('/create', response_model=UserOut)
async def create_user(user: UserIn, session: AsyncSession = session_depends) -> UserOut:
    return await crud.create_product(user, session)


@router.get('/all', response_model=User | None)
async def get_all_users(session: AsyncSession = session_depends) -> List[User] | None:
    return await crud.get_all_users(session)


@router.get('/{user_id}', response_model=User | None)
async def get_user(user_id: int, session: AsyncSession = session_depends) -> User | None:
    return await crud.get_user_by_id(user_id, session, is_formated=True)


@router.delete('/{user_id}', response_model=User)
async def delete_user(user_id: int, session: AsyncSession = session_depends) -> User:
    return await crud.delete_user(user_id, session)


@router.put('/{user_id}/update', response_model=User)
async def update_user(updated_user: UserIn, user_id: int, session: AsyncSession = session_depends) -> User:
    return await crud.update_user(updated_user, user_id, session)
