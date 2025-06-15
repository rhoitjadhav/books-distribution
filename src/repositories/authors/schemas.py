from typing import Optional

from repositories.base import BaseSchema


class AuthorsUpdateSchema(BaseSchema):
    name: str


class AuthorsSchema(AuthorsUpdateSchema):
    author_id: Optional[str]
    images: Optional[dict]


class ListAuthors(BaseSchema):
    authors: list[AuthorsSchema]
