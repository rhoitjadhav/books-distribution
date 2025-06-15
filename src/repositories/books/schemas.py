import enum
from typing import Optional

from repositories.base import BaseSchema


class CoverType(enum.Enum):
    PAPERBACK = "PAPERBACK"
    HARDBACK = "HARDBACK"


class BooksSchema(BaseSchema):
    book_id: Optional[str] = None
    book_title: str
    author_id: str
    publisher_id: str
    books_meta_data: Optional[dict]
    media_data: Optional[dict]
    pages: int
    publication_year: int
    price: int
    subject: str
    language: str
    cover_type: CoverType


class BooksUpdateSchema(BaseSchema):
    book_id: str
    book_title: Optional[str]
    author_id: Optional[str]
    publisher_id: Optional[str]
    books_meta_data: Optional[dict]
    media_data: Optional[dict]
    pages: Optional[int]
    publication_year: Optional[int]
    price: Optional[int]
    subject: Optional[str]
    language: Optional[str]
    cover_type: Optional[CoverType]
