from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class UserInDB(UserBase):
    password: str


class User(UserBase):
    id: int
