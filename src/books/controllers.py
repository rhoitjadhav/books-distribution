from fastapi import APIRouter, Response

from books.services import BooksService
from repositories.books.models import BooksModel
from repositories.books.schemas import BooksSchema, BooksUpdateSchema

router = APIRouter(prefix="/books")


@router.get("/{book_id}")
def get_book(book_id: str, response: Response):
    return BooksService(response, BooksModel).get_book(book_id)


@router.get("")
def list_books(response: Response, page: int = 1):
    return BooksService(response, BooksModel).list_books(page)


@router.post("")
def create_book(response: Response, book: BooksSchema):
    return BooksService(response, BooksModel).create_book(book)


@router.put("/{book_id}")
def update_book(book_id: str, book: BooksUpdateSchema, response: Response):
    return BooksService(response, BooksModel).update_book(book_id, book)
