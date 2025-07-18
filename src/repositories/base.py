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
    def get(cls, options: tuple = (), *filters, **kwargs) -> Any:
        """
        Retrieve a single record from the database with specific columns
        loaded, based on the provided filters and keyword arguments.
        """
        stmt = (
            select(cls).filter(*filters).options(*options).filter_by(**kwargs)
        )
        with SessionLocal() as session:
            return session.scalars(stmt).first()

    @classmethod
    def get_all(
        cls,
        limit: int = None,
        offset: int = None,
        options: list = (),
        *_,
        **kwargs,
    ) -> list:
        stmt = (
            select(cls)
            .filter_by(**kwargs)
            .limit(limit)
            .offset(offset)
            .options(*options)
        )
        with SessionLocal() as session:
            return session.scalars(stmt).unique().all()

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
