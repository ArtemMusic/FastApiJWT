from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from api_v1.users.schemas import User
from auth.helpers import create_access_token, create_refresh_token, REFRESH_TOKEN_TYPE
from auth.schemas import Token
from auth.validation import validate_auth_user, get_auth_user_from_token_of_type, get_current_token_payload

http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(
    prefix='/auth', tags=['JWT auth'], dependencies=[Depends(http_bearer)]
)


@router.post('/login', response_model=Token)
async def auth_user(user=Depends(validate_auth_user)) -> Token:
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.post('/refresh', response_model=Token, response_model_exclude_none=True)
def refresh_auth(user: User = Depends(get_auth_user_from_token_of_type(REFRESH_TOKEN_TYPE))) -> Token:
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.get('/user/me', response_model=dict)
def get_user_by_token(user=Depends(get_current_token_payload)) -> dict:
    return user
