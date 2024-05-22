from pydantic import BaseModel, ConfigDict, EmailStr


class UserPrivate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserDB(UserPrivate):
    id: int


class UserList(BaseModel):
    users: list[UserPublic]


class Message(BaseModel):
    detail: str
