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


class CartItemUpdateSchema(BaseSchema):
    quantity: int = 1


class CartItemAddSchema(CartItemUpdateSchema):
    book_id: str


class CartItemResponseSchema(CartItemAddSchema):
    cart_item_id: Optional[UUID]
    cart_id: UUID
    created_at: datetime
    updated_at: datetime


class CartItemsDetailSchema(BaseSchema):
    cart_item_id: Optional[UUID]
    cart_id: UUID
    book: BooksSchema
    quantity: int


class CartItemDeleteSchema(BaseSchema):
    cart_item_id: UUID
