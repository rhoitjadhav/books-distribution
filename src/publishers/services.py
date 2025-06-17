from fastapi.openapi.models import Response

from common.helper import to_dict
from common.schemas import ErrorSchema
from repositories.publishers.models import PublishersModel
from repositories.publishers.schemas import ListPublishers, PublishersSchema


class PublishersService:
    def __init__(
        self, response: Response, publishers_repository: PublishersModel
    ):
        self._publishers_repository = publishers_repository
        self._response = response

    def list_publishers(self, page: int, page_size: int = 10):
        limit = page_size * page
        offset = (page - 1) * page_size
        publishers = self._publishers_repository.get_all(limit, offset)
        publishers = [
            PublishersSchema.model_validate(to_dict(publisher))
            for publisher in publishers
        ]
        return ListPublishers(publishers=publishers)

    def get_publisher(self, publisher_id: int):
        publisher = self._publishers_repository.get_by_pk(publisher_id)
        if not publisher:
            self._response.status_code = 404
            return ErrorSchema(message="Publisher not found")
        return PublishersSchema.model_validate(to_dict(publisher))

    def create_publisher(self, publisher: PublishersSchema):
        return self._publishers_repository.create(**publisher.model_dump())

    def update_publisher(self, publisher_id: str, publisher: PublishersSchema):
        return self._publishers_repository.update(
            publisher_id, **publisher.model_dump()
        )
