from fastapi import Response

from common.helper import to_dict, get_limit_offset
from common.schemas import ErrorSchema
from repositories.books.models import BooksModel
from repositories.books.schemas import BooksSchema, BooksUpdateSchema


class BooksService:
    def __init__(self, response: Response, books_repository: BooksModel):
        self._books_repository = books_repository
        self._response = response

    def list_books(self, page: int, page_size: int):
        limit, offset = get_limit_offset(page, page_size)
        books = self._books_repository.get_all(limit, offset)
        books = [BooksSchema.model_validate(to_dict(book)) for book in books]
        return books

    def get_book(self, book_id):
        book = self._books_repository.get_by_pk(book_id)
        if not book:
            self._response.status_code = 404
            return ErrorSchema(message="Book not found")
        return BooksSchema.model_validate(to_dict(book))

    def create_book(self, book: BooksSchema):
        if not book.book_id:
            book.book_id = self._books_repository.generate_book_id()
        book = self._books_repository.create(**book.model_dump())
        return BooksSchema.model_validate(book)

    def update_book(self, book_id: str, book: BooksUpdateSchema):
        return self._books_repository.update(book_id, **book.model_dump())
