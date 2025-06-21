import random
import string

from sqlalchemy import Column, Integer, String, ForeignKey, Enum, select
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from common.exceptions import NotFoundException
from common.helper import to_dict
from database import SessionLocal
from repositories.base import BaseModel
from repositories.books.schemas import CoverType


class BooksModel(BaseModel):
    __tablename__ = "books"

    book_id = Column(String, primary_key=True)
    book_title = Column(String(255), nullable=False)
    author_id = Column(String, ForeignKey("authors.author_id"), nullable=False)
    publisher_id = Column(
        String, ForeignKey("publishers.publisher_id"), nullable=False
    )
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
    def generate_book_id():
        """
        Generate book ID string with format:
        - b, stands for book
        - 7 random uppercase alphanumeric chars

        Example
        -------
        bji5bqsr
            b + ji5bqsr (random)
        """
        ALPHANUMERIC = string.ascii_uppercase + string.digits
        random_chars = "".join(random.choices(ALPHANUMERIC, k=7))
        return f"b{random_chars}"

    @staticmethod
    def get_by_pk(pk: str) -> "BooksModel":
        stmt = select(BooksModel).where(BooksModel.book_id == pk)
        with SessionLocal() as session:
            return session.scalars(stmt).first()

    @staticmethod
    def update(pk: str, **kwargs) -> "BooksModel":
        with SessionLocal() as session:
            book = session.get(BooksModel, pk)
            if not book:
                raise NotFoundException(f"Book not found for id: {pk}")
            for key, value in kwargs.items():
                setattr(book, key, value)
            session.commit()
            return to_dict(book)
