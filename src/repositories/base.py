from __future__ import annotations

from typing import Any

import humps
from sqlalchemy import select, delete
from pydantic import BaseModel as PydanticBaseModel

from common.helper import to_dict
from database import Base, SessionLocal


class BaseModel(Base):
    __abstract__ = True

    @classmethod
    def get(cls, **kwargs) -> Any:
        """
        Retrieve a single record from the database based on the
        provided keyword arguments.
        """
        stmt = select(cls).filter_by(**kwargs)
        with SessionLocal() as session:
            return session.scalars(stmt).first()

    @classmethod
    def get_all(
        cls, limit: int = None, offset: int = None, *_, **kwargs
    ) -> list:
        stmt = select(cls).filter_by(**kwargs).limit(limit).offset(offset)
        with SessionLocal() as session:
            return session.scalars(stmt).all()

    @classmethod
    def create(cls, **kwargs) -> dict:
        model_obj = cls(**kwargs)
        with SessionLocal() as session:
            session.add(model_obj)
            session.commit()
            session.refresh(model_obj)
            return to_dict(model_obj)

    @classmethod
    def delete(cls, *filters):
        stmt = delete(cls).where(*filters)
        with SessionLocal() as session:
            result = session.execute(stmt)
            session.commit()
            return result.rowcount


class BaseSchema(PydanticBaseModel):
    class Config:
        alias_generator = humps.camelize
        populate_by_name = True
