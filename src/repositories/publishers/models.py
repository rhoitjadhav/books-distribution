from sqlalchemy import Column, String, select
from sqlalchemy.exc import NoResultFound

from common.helper import to_dict, get_random_str
from database import Base, SessionLocal


class PublishersModel(Base):
    __tablename__ = "publishers"

    publisher_id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)

    def __repr__(self):
        return f"<Publisher {self.name}>"

    @staticmethod
    def get_by_pk(pk: str) -> "PublishersModel":
        stmt = select(PublishersModel).where(PublishersModel.publisher_id == pk)
        with SessionLocal() as session:
            return session.scalars(stmt).first()

    @staticmethod
    def get(**kwargs) -> "PublishersModel":
        stmt = select(PublishersModel).filter_by(**kwargs)
        with SessionLocal() as session:
            return session.scalars(stmt).first()

    @staticmethod
    def get_all(limit: int, offset: int, **kwargs) -> list["PublishersModel"]:
        stmt = select(PublishersModel).filter_by(**kwargs).limit(limit).offset(offset)
        with SessionLocal() as session:
            return session.scalars(stmt).all()

    @staticmethod
    def create(**kwargs) -> dict:
        publisher = PublishersModel(**kwargs)
        publisher.publisher_id = get_random_str()
        with SessionLocal() as session:
            session.add(publisher)
            session.commit()
            return to_dict(publisher)

    @staticmethod
    def update(pk: str, **kwargs) -> dict:
        with SessionLocal() as session:
            publisher = session.get(PublishersModel, pk)
            if not publisher:
                raise NoResultFound(f"Publisher not found for id: {pk}")
            for key, value in kwargs.items():
                setattr(publisher, key, value)
            session.commit()
            return to_dict(publisher)
