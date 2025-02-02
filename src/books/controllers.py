from fastapi import APIRouter, Response

from books.services import BooksService
from repositories.books.models import BooksModel

router = APIRouter(prefix="/books")


@router.get("/{book_id}")
def get_book(book_id: str, response: Response):
    return BooksService(response, BooksModel).get_book(book_id)


@router.get("")
def list_books(response: Response, page: int = 1, page_size: int = 10):
    return BooksService(response, BooksModel).list_books(page, page_size)


@router.post("")
def create_book():
    return {"book": "book"}


@router.put("/{book_id}")
def update_book(book_id: str):
    return {"book": "book"}
