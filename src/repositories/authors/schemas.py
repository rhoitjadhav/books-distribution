from typing import Optional

from pydantic import BaseModel


class AuthorsUpdateSchema(BaseModel):
    name: str


class AuthorsSchema(AuthorsUpdateSchema):
    author_id: Optional[str]
    images: Optional[dict]


class ListAuthors(BaseModel):
    authors: list[AuthorsSchema]
