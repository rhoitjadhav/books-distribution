from fastapi import Response

from common.helper import to_dict
from common.schemas import ErrorSchema
from repositories.authors.models import AuthorsModel
from repositories.authors.schemas import ListAuthors, AuthorsSchema


class AuthorsService:
    def __init__(self, response: Response, authors_repository: AuthorsModel):
        self._authors_repository = authors_repository
        self._response = response

    def list_authors(self, page: int, page_size: int):
        limit = page_size * page
        offset = (page - 1) * page_size
        authors = self._authors_repository.get_all(limit, offset)
        authors = [AuthorsSchema.model_validate(to_dict(author)) for author in authors]
        return ListAuthors(authors=authors)

    def get_author(self, author_id: str):
        author = self._authors_repository.get_by_pk(author_id)
        if not author:
            self._response.status_code = 404
            return ErrorSchema(message="Author not found")
        return AuthorsSchema.model_validate(to_dict(author))

    def create_author(self, author: AuthorsSchema):
        return self._authors_repository.create(**author.model_dump())

    def update_author(self, author_id: str, author: AuthorsSchema):
        return self._authors_repository.update(author_id, **author.model_dump())
