from uuid import UUID

from pydantic import EmailStr

from repositories.base import BaseSchema


class UserInfoSchema(BaseSchema):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    isd_code: str

    # TODO: Add validation for phone number format


class RegisterUserSchema(UserInfoSchema):
    password: str


class UsersSchema(UserInfoSchema):
    user_id: UUID
    is_guest: bool


class SignInSchema(BaseSchema):
    email: EmailStr
    password: str


class SignInResponseSchema(BaseSchema):
    user_id: UUID
    access_token: str
    token_type: str = "bearer"
    message: str = "Sign in successful"
