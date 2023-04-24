from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserModel(BaseModel):
    full_name: str | None = None
    email: str | None = None
    username: str | None = None
    password: str | None = None
    disabled: bool | None = None


class UserInDB(UserModel):
    hashed_password: str
