from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from repositories.books.models import CoverType


class BooksSchema(BaseModel):
    book_id: Optional[UUID]
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


class BooksUpdateSchema(BaseModel):
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


class ListBooks(BaseModel):
    books: list[BooksSchema]
