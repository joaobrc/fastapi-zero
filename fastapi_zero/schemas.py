from pydantic import BaseModel, EmailStr


class UserPrivate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    username: str
    email: EmailStr