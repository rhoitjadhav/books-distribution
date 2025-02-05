import enum
import uuid

from sqlalchemy import Column, Integer, String, ForeignKey, UUID, Enum, select
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import relationship

from common.helper import to_dict
from database import Base, SessionLocal


class CoverType(enum.Enum):
    PAPERBACK = "PAPERBACK"
    HARDBACK = "HARDBACK"


class BooksModel(Base):
    __tablename__ = "books"

    book_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    book_title = Column(String(255), nullable=False)
    author_id = Column(String, ForeignKey("authors.author_id"), nullable=False)
    publisher_id = Column(String, ForeignKey("publishers.publisher_id"), nullable=False)
    books_meta_data = Column(JSONB, nullable=True)
    media_data = Column(JSONB, nullable=True)
    pages = Column(Integer, nullable=False)
    publication_year = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    subject = Column(String(255), nullable=False)
    language = Column(String(100), nullable=False)
    cover_type = Column(Enum(CoverType, name="cover_types"), nullable=False)

    # Relationships
    author = relationship("AuthorsModel", backref="books")
    publisher = relationship("PublishersModel", backref="books")

    def __repr__(self):
        return f"<Book {self.book_title} ({self.publication_year})>"

    @staticmethod
    def get_by_pk(pk: str) -> "BooksModel":
        stmt = select(BooksModel).where(BooksModel.book_id == pk)
        with SessionLocal() as session:
            return session.scalars(stmt).first()

    @staticmethod
    def get(**kwargs) -> "BooksModel":
        stmt = select(BooksModel).filter_by(**kwargs)
        with SessionLocal() as session:
            return session.scalars(stmt).first()

    @staticmethod
    def get_all(limit: int, offset: int, **kwargs) -> list["BooksModel"]:
        stmt = select(BooksModel).filter_by(**kwargs).limit(limit).offset(offset)
        with SessionLocal() as session:
            return session.scalars(stmt).all()

    @staticmethod
    def create(**kwargs) -> dict:
        book = BooksModel(**kwargs)
        with SessionLocal() as session:
            session.add(book)
            session.commit()
            return to_dict(book)

    @staticmethod
    def update(pk: str, **kwargs) -> "BooksModel":
        with SessionLocal() as session:
            book = session.get(BooksModel, pk)
            if not book:
                raise NoResultFound(f"Book not found for id: {pk}")
            for key, value in kwargs.items():
                setattr(book, key, value)
            session.commit()
            return to_dict(book)
