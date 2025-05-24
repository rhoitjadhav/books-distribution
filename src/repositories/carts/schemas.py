from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from repositories.books.schemas import BooksSchema


class CartSchema(BaseModel):
    id: Optional[UUID]
    user_id: UUID
    created_at: datetime
    updated_at: datetime


class CartItemSchema(BaseModel):
    book_id: UUID = "75e8b351-f612-4eff-8dfe-6544e73a8df4"  # remove this default value
    quantity: Optional[int] = 1


class CartItemsDetailSchema(BaseModel):
    id: Optional[UUID]
    cart_id: UUID
    book: BooksSchema
    quantity: int
    price: float


class CartItemDeleteSchema(BaseModel):
    cart_item_id: UUID
