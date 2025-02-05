from fastapi import APIRouter, Response

from authors.services import AuthorsService
from repositories.authors.models import AuthorsModel
from repositories.authors.schemas import AuthorsUpdateSchema

router = APIRouter(prefix="/authors")


@router.get("/{author_id}")
def get_author(author_id: str, response: Response):
    return AuthorsService(response, AuthorsModel).get_author(author_id)


@router.get("")
def list_authors(response: Response, page: int = 1, page_size: int = 10):
    return AuthorsService(response, AuthorsModel).list_authors(page, page_size)


@router.post("")
def create_author(response: Response, author: AuthorsUpdateSchema):
    return AuthorsService(response, AuthorsModel).create_author(author)


@router.put("/{author_id}")
def update_author(author_id: str, response: Response, author: AuthorsUpdateSchema):
    return AuthorsService(response, AuthorsModel).update_author(author_id, author)
