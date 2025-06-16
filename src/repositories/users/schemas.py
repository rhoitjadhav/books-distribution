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


class UsersSchema(UserInfoSchema):
    user_id: UUID
    is_guest: bool
