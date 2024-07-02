from datetime import datetime

from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
    username: str
    email: EmailStr


class User(UserBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class UserOut(UserBase):
    username: str
    email: EmailStr
    created_at: datetime


class UserIn(UserBase):
    username: str
    email: EmailStr
    password: str
