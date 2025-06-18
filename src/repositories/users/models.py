import uuid

from passlib.context import CryptContext
from sqlalchemy import Column, String, Boolean, DateTime, func, UUID, select
from sqlalchemy.orm import load_only

from common.helper import to_dict
from database import SessionLocal
from repositories.base import BaseModel


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UsersModel(BaseModel):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String, nullable=True, index=True)
    last_name = Column(String, index=True)
    email = Column(String(255), unique=True, nullable=False)
    _password = Column("password", String, nullable=True)
    isd_code = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    is_guest = Column(Boolean, default=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, plain_password: str):
        self._password = pwd_context.hash(plain_password)

    def verify_password(self, plain_password: str) -> bool:
        return pwd_context.verify(plain_password, self._password)

    @staticmethod
    def is_email_exists(email: str):
        """
        Check if the provided email already exists in the database.
        Returns True if the email exists, otherwise False.
        """
        stmt = (
            select(UsersModel)
            .filter_by(email=email)
            .options(load_only(UsersModel.email))
        )
        with SessionLocal() as session:
            return session.scalars(stmt).first()

    def create_or_get(self, **kwargs):
        """
        Create a new user or retrieve an existing one based on the provided
        email. If the user already exists, it returns the existing user.
        If not, it creates a new user with the provided details.
        """
        stmt = select(UsersModel).filter_by(email=kwargs.get("email"))
        with SessionLocal() as session:
            user = session.scalars(stmt).first()
            return to_dict(user) if user else self.create(**kwargs)
