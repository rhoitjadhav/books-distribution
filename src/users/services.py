from common.exceptions import ConflictException, NotFoundException
from common.schemas import ResponseSchema
from repositories.users.models import UsersModel
from repositories.users.schemas import (
    UserInfoSchema,
    UsersSchema,
    SignInSchema,
    SignInResponseSchema,
)
from auth.services import AuthService


class UsersService:
    def __init__(
        self, users_repository: UsersModel, auth_service: AuthService = None
    ):
        self._users_repository = users_repository
        self._auth_service = auth_service

    def register_user(self, user_info: UserInfoSchema):
        if self._users_repository.is_email_exists(user_info.email):
            raise ConflictException("Email already exists")

        kwargs = {
            **user_info.model_dump(),
            "is_guest": False,
        }
        user = UsersSchema.model_validate(
            self._users_repository.create(**kwargs)
        )
        return ResponseSchema(
            user_id=user.user_id, message="User created successfully"
        )

    def sign_in(self, user_in: SignInSchema):
        from sqlalchemy.orm import load_only

        user = self._users_repository.get(
            options=[load_only(UsersModel.email, UsersModel._password)],
            email=user_in.email,
        )
        if not user or not user.verify_password(user_in.password):
            raise NotFoundException("Invalid email or password")

        access_token = self._auth_service.create_access_token(
            {"sub": str(user.user_id)}
        )
        return SignInResponseSchema(
            user_id=user.user_id, access_token=access_token
        )
