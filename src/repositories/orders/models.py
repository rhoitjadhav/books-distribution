from __future__ import annotations

import random
import string
import uuid
from datetime import datetime

from sqlalchemy import (
    ForeignKey,
    Integer,
    String,
    Float,
    DateTime,
    func,
    Column,
    UUID,
)
from sqlalchemy.orm import relationship

from common.helper import to_dict
from database import Base, SessionLocal
from repositories.carts.models import CartItemsModel


class OrdersModel(Base):
    __tablename__ = "orders"

    order_id = Column(String, primary_key=True)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    total_amount = Column(Float, nullable=False)
    status = Column(String(50), nullable=False, default="PENDING")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    items = relationship(
        "OrderItemsModel", back_populates="order", cascade="all, delete-orphan"
    )

    @staticmethod
    def generate_order_id():
        """
        Generate order ID string with format:
        - BO, stands for Pelago Order
        - YY, year created
        - mm, month created
        - 6 random uppercase alphanumeric chars

        Example
        -------
        BO2501JI5BQS
            BO + 25 (year) + 01 (month) + JI5BQS (random)
        """
        now = datetime.now()
        year = now.strftime("%y")
        month = now.strftime("%m")

        ALPHANUMERIC = string.ascii_uppercase + string.digits
        random_chars = "".join(random.choices(ALPHANUMERIC, k=6))
        return f"BO{year}{month}{random_chars}"

    @staticmethod
    def create(session=True, **kwargs) -> dict | OrdersModel:
        order = OrdersModel(**kwargs)
        if not session:
            return order

        with SessionLocal() as session:
            session.add(order)
            session.commit()
            return to_dict(order)


class OrderItemsModel(Base):
    __tablename__ = "order_items"

    order_item_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    order_id = Column(String, ForeignKey("orders.order_id"), nullable=False, index=True)
    book_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    order = relationship("OrdersModel", back_populates="items")

    @staticmethod
    def create(**kwargs) -> "OrderItemsModel":
        order_item = OrderItemsModel(**kwargs)
        with SessionLocal() as session:
            session.add(order_item)
            session.commit()
            return to_dict(order_item)

    @staticmethod
    def create_order_items(
        order_kwargs: dict, items: list[CartItemsModel]
    ) -> list[dict]:
        order = OrdersModel(**order_kwargs)
        order_items = [
            OrderItemsModel(
                order_id=order.order_id,
                book_id=item.book_id,
                quantity=item.quantity,
                price=item.book.price,
            )
            for item in items
        ]

        with SessionLocal() as session:
            session.add(order)
            session.add_all(order_items)
            session.commit()
            return to_dict(order), [to_dict(item) for item in order_items]
