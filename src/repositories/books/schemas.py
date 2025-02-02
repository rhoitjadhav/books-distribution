from pydantic import BaseModel


class BooksSchema(BaseModel):
    title: str
    author_id: str
    publisher_id: str
    books_meta_data: dict
    media_data: dict
    pages: int
    publication_year: int
    price: int
    subject: str


class ListBooks(BaseModel):
    books: list[BooksSchema]
