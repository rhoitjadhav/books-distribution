from fastapi import Response

from common.schemas import ErrorSchema
from repositories.books.models import BooksModel
from repositories.books.schemas import BooksSchema, ListBooks


class BooksService:
    def __init__(self, response: Response, books_repository: BooksModel):
        self._books_repository = books_repository
        self._response = response

    def list_books(self, page: int, page_size: int):
        limit = page_size * page
        offset = (page - 1) * page_size
        books = self._books_repository.get_all(limit, offset)
        return ListBooks(books=books)

    def get_book(self, book_id):
        book = self._books_repository.get_by_pk(book_id)
        if not book:
            self._response.status_code = 404
            return ErrorSchema(message="Book not found")
        return BooksSchema.model_validate(book)

    def create_book(self, book: BooksSchema):
        return self._books_repository.create(book.model_dump_json())

    def update_book(self, book_id, book):
        return self._books_repository.update(book_id, book)
