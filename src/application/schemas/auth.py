from pydantic import BaseModel


class SignUpDetails(BaseModel):
    user_id: int
    message: str
    email: str
    name: str
    photo_url: str | None


class LoginDetails(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    message: str
    email: str
    access_token: str
