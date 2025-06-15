from typing import Optional

from repositories.base import BaseSchema


class PublishersUpdateSchema(BaseSchema):
    name: str
    address: str


class PublishersSchema(PublishersUpdateSchema):
    publisher_id: Optional[str]
    address: Optional[str]


class ListPublishers(BaseSchema):
    publishers: list[PublishersSchema]
