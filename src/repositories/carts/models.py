import uuid

from sqlalchemy import (
    ForeignKey,
    Integer,
    DateTime,
    func,
    Column,
    UUID,
    select,
    String,
)
from sqlalchemy.orm import relationship, joinedload

from common.exceptions import NotFoundException
from common.helper import to_dict
from database import SessionLocal
from repositories.base import BaseModel


class CartsModel(BaseModel):
    __tablename__ = "carts"

    cart_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    items = relationship(
        "CartItemsModel", back_populates="cart", cascade="all, delete-orphan"
    )


class CartItemsModel(BaseModel):
    __tablename__ = "cart_items"

    cart_item_id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    cart_id = Column(
        UUID(as_uuid=True),
        ForeignKey("carts.cart_id"),
        nullable=False,
        index=True,
    )
    book_id = Column(String, ForeignKey("books.book_id"))
    quantity = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    cart = relationship("CartsModel", back_populates="items")
    book = relationship("BooksModel")

    @classmethod
    def get_all(
        cls, limit: int = None, offset: int = None, *args, **kwargs
    ) -> list:
        stmt = (
            select(CartItemsModel)
            .filter(*args)
            .filter_by(**kwargs)
            .limit(limit)
            .offset(offset)
        )
        with SessionLocal() as session:
            return session.scalars(stmt).all()

    @staticmethod
    def update(pk: str, **kwargs) -> "CartItemsModel":
        with SessionLocal() as session:
            cart_item = session.get(CartItemsModel, pk)
            if not cart_item:
                raise NotFoundException(f"Cart item not found for id: {pk}")
            for key, value in kwargs.items():
                setattr(cart_item, key, value)
            session.commit()
            return to_dict(cart_item)

    @staticmethod
    def get_cart_items(
        user_id: str, limit: int = 10, offset: int = 0, *filters
    ) -> list["CartItemsModel"]:
        stmt = (
            select(CartItemsModel)
            .options(joinedload(CartItemsModel.book))
            .join(CartsModel, CartsModel.cart_id == CartItemsModel.cart_id)
            .where(
                CartsModel.user_id == user_id,
                *filters,
            )
            .limit(limit)
            .offset(offset)
        )
        with SessionLocal() as session:
            return session.scalars(stmt).all()
