from datetime import datetime
from uuid import UUID

from common.utils import EnumBase
from repositories.base import BaseSchema
from repositories.books.schemas import BookMetaDataSchema
from repositories.user_addresses.schemas import AddressRequestSchema
from repositories.users.schemas import UserInfoSchema


class OrderStatus(EnumBase):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"


class OrdersSchema(BaseSchema):
    order_id: str
    user_id: UUID
    total_amount: float
    status: str
    created_at: datetime = None
    updated_at: datetime = None


class OrderItemsSchema(BaseSchema):
    order_item_id: UUID | None = None
    order_id: str
    book_id: str
    book_meta_data: BookMetaDataSchema
    quantity: int
    total_amount: float
    created_at: datetime = None
    updated_at: datetime = None


class CheckoutRequestSchema(BaseSchema):
    cart_item_ids: list[str]
    user_info: UserInfoSchema
    address_id: str | None = None
    address_info: AddressRequestSchema | None = None


class OrderDetailsSchema(BaseSchema):
    order_id: str
    order_amount: float
    status: str
    address_meta_data: dict
    user_meta_data: dict
    items: list[OrderItemsSchema]
