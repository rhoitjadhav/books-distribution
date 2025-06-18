from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/users/sign-in")


async def get_jwt_sub(token: str = Depends(oauth2_scheme)) -> str | None:
    import os
    from config import get_env_config
    from auth.services import AuthService

    config = get_env_config(os.getenv("ENV", "dev"))
    auth_service = AuthService(
        config.JWT_SECRET_KEY,
        config.JWT_ALGORITHM,
        config.JWT_ACCESS_TOKEN_EXPIRE,
    )
    payload = auth_service.decode_access_token(token)
    return payload.get("sub")
