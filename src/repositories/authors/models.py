from sqlalchemy import Column, String, select
from sqlalchemy.dialects.postgresql import JSONB

from common.exceptions import NotFoundException
from common.helper import get_random_str, to_dict
from database import SessionLocal
from repositories.base import BaseModel


class AuthorsModel(BaseModel):
    __tablename__ = "authors"

    author_id = Column(String, primary_key=True, default=get_random_str)
    name = Column(String, nullable=False)
    images = Column(JSONB, nullable=True)

    def __repr__(self):
        return f"<Author {self.name}>"

    @staticmethod
    def get_by_pk(pk: str) -> "AuthorsModel":
        stmt = select(AuthorsModel).where(AuthorsModel.author_id == pk)
        with SessionLocal() as session:
            return session.scalars(stmt).first()

    @staticmethod
    def update(pk: str, **kwargs) -> dict:
        with SessionLocal() as session:
            author = session.get(AuthorsModel, pk)
            if not author:
                raise NotFoundException(f"Author not found for id: {pk}")
            for key, value in kwargs.items():
                setattr(author, key, value)
            session.commit()
            return to_dict(author)
