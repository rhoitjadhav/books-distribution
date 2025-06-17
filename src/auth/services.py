from datetime import timedelta, datetime, UTC

from jose import jwt

from common.exceptions import TokenInvalidException


class AuthService:
    def __init__(
        self, secret_key: str, algorithm: str, access_token_expire: int
    ):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire = access_token_expire

    def create_access_token(
        self, data: dict, expires_delta: timedelta | None = None
    ) -> str:
        to_encode = data.copy()
        expire = datetime.now(UTC) + (
            expires_delta or timedelta(minutes=self.access_token_expire)
        )
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def decode_access_token(self, token: str) -> dict:
        try:
            return jwt.decode(
                token, self.secret_key, algorithms=[self.algorithm]
            )
        except Exception as e:
            raise TokenInvalidException(str(e))
