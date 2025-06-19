from uuid import UUID

from repositories.base import BaseSchema


class AddressRequestSchema(BaseSchema):
    full_name: str
    address_line_1: str
    address_line_2: str | None = None
    city: str
    state: str
    postal_code: str
    country: str
    phone: str
    isd_code: str


class AddressSchema(AddressRequestSchema):
    address_id: UUID
