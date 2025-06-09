import humps
from sqlalchemy import select
from pydantic import BaseModel as PydanticBaseModel
from database import Base, SessionLocal


class BaseModel(Base):
    __abstract__ = True

    @classmethod
    def get(cls, **kwargs):
        """
        Retrieve a single record from the database based on the
        provided keyword arguments.
        """
        stmt = select(cls).filter_by(**kwargs)
        with SessionLocal() as session:
            return session.scalars(stmt).first()

    @classmethod
    def get_all(cls, limit: int = None, offset: int = None, **kwargs):
        stmt = select(cls).filter_by(**kwargs).limit(limit).offset(offset)
        with SessionLocal() as session:
            return session.scalars(stmt).all()


class BaseSchema(PydanticBaseModel):
    class Config:
        alias_generator = humps.camelize
        populate_by_name = True
