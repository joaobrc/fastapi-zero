from pydantic import BaseModel, EmailStr


class UserPrivate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr


class UserDB(UserPrivate):
    id: int


class UserList(BaseModel):
    users: list[UserPublic]


class Message(BaseModel):
    detail: str
