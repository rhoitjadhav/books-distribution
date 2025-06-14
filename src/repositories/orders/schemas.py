from datetime import datetime
from uuid import UUID

from common.utils import EnumBase
from repositories.base import BaseSchema


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
    order_item_id: UUID
    order_id: str
    book_id: str
    book_meta_data: dict
    quantity: int
    price: float
    created_at: datetime = None
    updated_at: datetime = None
