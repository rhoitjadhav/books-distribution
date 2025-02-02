from typing import Optional

from pydantic import BaseModel

from repositories.books.models import CoverType


class BooksSchema(BaseModel):
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


class ListBooks(BaseModel):
    books: list[BooksSchema]
