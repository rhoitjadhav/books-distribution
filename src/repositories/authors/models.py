import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import JSONB

from database import Base


class AuthorsModel(Base):
    __tablename__ = "authors"

    author_id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    images = Column(JSONB, nullable=True)

    def __repr__(self):
        return f"<Author {self.name}>"
