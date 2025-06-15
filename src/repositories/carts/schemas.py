from datetime import datetime
from typing import Optional
from uuid import UUID

from repositories.base import BaseSchema
from repositories.books.schemas import BooksSchema


class CartSchema(BaseSchema):
    cart_id: Optional[UUID]
    user_id: UUID
    created_at: datetime
    updated_at: datetime


class CartItemSchema(BaseSchema):
    book_id: str = (
        "75e8b351-f612-4eff-8dfe-6544e73a8df4"  # remove this default value
    )
    quantity: Optional[int] = 1


class CartItemsDetailSchema(BaseSchema):
    cart_item_id: Optional[UUID]
    cart_id: UUID
    book: BooksSchema
    quantity: int


class CartItemDeleteSchema(BaseSchema):
    cart_item_id: UUID
