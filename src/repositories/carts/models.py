import uuid

from sqlalchemy import (
    ForeignKey,
    Integer,
    Float,
    DateTime,
    func,
    Column,
    UUID,
)
from sqlalchemy.orm import relationship

from database import Base


class CartsModels(Base):
    __tablename__ = "carts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    items = relationship(
        "CartItemsModel", back_populates="cart", cascade="all, delete-orphan"
    )


class CartItemsModel(Base):
    __tablename__ = "cart_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cart_id = Column(
        UUID(as_uuid=True), ForeignKey("carts.id"), nullable=False, index=True
    )
    book_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    quantity = Column(Integer, nullable=False, default=1)
    price = Column(Float, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    cart = relationship("CartsModel", back_populates="items")
