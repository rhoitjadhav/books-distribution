from typing import Optional

from pydantic import BaseModel


class PublishersUpdateSchema(BaseModel):
    name: str
    address: str


class PublishersSchema(PublishersUpdateSchema):
    publisher_id: Optional[str]
    address: Optional[str]


class ListPublishers(BaseModel):
    publishers: list[PublishersSchema]
