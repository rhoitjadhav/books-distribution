import os

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from repositories.users.models import UsersModel
from repositories.users.schemas import RegisterUserSchema, SignInSchema
from users.services import UsersService
from auth.services import AuthService
from config import get_env_config

router = APIRouter(prefix="/users")
config = get_env_config(os.getenv("BE_ENV", "dev"))


@router.post("/register")
async def register_user(user_info: RegisterUserSchema):
    return UsersService(UsersModel()).register_user(user_info)


@router.post("/sign-in")
async def sign_in(form_data: OAuth2PasswordRequestForm = Depends()):
    user = SignInSchema(email=form_data.username, password=form_data.password)
    return UsersService(
        UsersModel(),
        AuthService(
            config.JWT_SECRET_KEY,
            config.JWT_ALGORITHM,
            config.JWT_ACCESS_TOKEN_EXPIRE,
        ),
    ).sign_in(user)
