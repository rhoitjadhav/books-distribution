from sqlalchemy import Column, String, select

from common.exceptions import NotFoundException
from common.helper import to_dict, get_random_str
from database import SessionLocal
from repositories.base import BaseModel


class PublishersModel(BaseModel):
    __tablename__ = "publishers"

    publisher_id = Column(String, primary_key=True, default=get_random_str)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)

    def __repr__(self):
        return f"<Publisher {self.name}>"

    @staticmethod
    def get_by_pk(pk: str) -> "PublishersModel":
        stmt = select(PublishersModel).where(
            PublishersModel.publisher_id == pk
        )
        with SessionLocal() as session:
            return session.scalars(stmt).first()

    @staticmethod
    def update(pk: str, **kwargs) -> dict:
        with SessionLocal() as session:
            publisher = session.get(PublishersModel, pk)
            if not publisher:
                raise NotFoundException(f"Publisher not found for id: {pk}")
            for key, value in kwargs.items():
                setattr(publisher, key, value)
            session.commit()
            return to_dict(publisher)
