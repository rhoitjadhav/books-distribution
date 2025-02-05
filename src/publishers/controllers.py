from fastapi import APIRouter, Response

from publishers.services import PublishersService
from repositories.publishers.models import PublishersModel
from repositories.publishers.schemas import PublishersUpdateSchema

router = APIRouter(prefix="/publishers")


@router.get("/{publisher_id}")
def get_publisher(publisher_id: str, response: Response):
    return PublishersService(response, PublishersModel).get_publisher(publisher_id)


@router.get("")
def list_publishers(response: Response, page: int = 1, page_size: int = 10):
    return PublishersService(response, PublishersModel).list_publishers(page, page_size)


@router.post("")
def create_publisher(response: Response, publisher: PublishersUpdateSchema):
    return PublishersService(response, PublishersModel).create_publisher(publisher)


@router.put("/{publisher_id}")
def update_publisher(
    publisher_id: str, response: Response, publisher: PublishersUpdateSchema
):
    return PublishersService(response, PublishersModel).update_publisher(
        publisher_id, publisher
    )
