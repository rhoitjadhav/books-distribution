import uuid

from sqlalchemy import (
    ForeignKey,
    Integer,
    DateTime,
    func,
    Column,
    UUID,
    select,
)
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import relationship, selectinload, joinedload

from common.helper import to_dict
from database import Base, SessionLocal


class CartsModel(Base):
    __tablename__ = "carts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    items = relationship(
        "CartItemsModel", back_populates="cart", cascade="all, delete-orphan"
    )

    @staticmethod
    def get(**kwargs) -> "CartsModel":
        lazy_load = kwargs.pop("lazy_load", False)
        stmt = (
            select(CartsModel)
            .filter_by(**kwargs)
            .options(selectinload(CartsModel.items))
            if lazy_load
            else select(CartsModel).filter_by(**kwargs)
        )

        with SessionLocal() as session:
            return session.scalars(stmt).first()

    @staticmethod
    def create(**kwargs) -> "CartsModel":
        cart = CartsModel(**kwargs)
        with SessionLocal() as session:
            session.add(cart)
            session.commit()
            return to_dict(cart)


class CartItemsModel(Base):
    __tablename__ = "cart_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cart_id = Column(
        UUID(as_uuid=True), ForeignKey("carts.id"), nullable=False, index=True
    )
    book_id = Column(UUID(as_uuid=True), ForeignKey("books.book_id"))
    quantity = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    cart = relationship("CartsModel", back_populates="items")
    book = relationship("BooksModel")

    @staticmethod
    def get(**kwargs) -> "CartItemsModel":
        stmt = select(CartItemsModel).filter_by(**kwargs)
        with SessionLocal() as session:
            return session.scalars(stmt).first()

    @staticmethod
    def get_all(limit: int, offset: int, **kwargs) -> list["CartItemsModel"]:
        stmt = select(CartItemsModel).filter_by(**kwargs).limit(limit).offset(offset)
        with SessionLocal() as session:
            return session.scalars(stmt).all()

    @staticmethod
    def create(**kwargs) -> "CartItemsModel":
        cart_item = CartItemsModel(**kwargs)
        with SessionLocal() as session:
            session.add(cart_item)
            session.commit()
            return to_dict(cart_item)

    @staticmethod
    def update(pk: str, **kwargs) -> "CartItemsModel":
        with SessionLocal() as session:
            cart_item = session.get(CartItemsModel, pk)
            if not cart_item:
                raise NoResultFound(f"Cart item not found for id: {pk}")
            for key, value in kwargs.items():
                setattr(cart_item, key, value)
            session.commit()
            return to_dict(cart_item)

    @staticmethod
    def delete(**kwargs):
        with SessionLocal() as session:
            cart_item = session.scalars(
                select(CartItemsModel).filter_by(**kwargs)
            ).first()
            if not cart_item:
                raise ValueError("Cart item not found")
            session.delete(cart_item)
            session.commit()
            return to_dict(cart_item)

    @staticmethod
    def get_cart_items(
        user_id: str, limit: int = 10, offset: int = 0
    ) -> list["CartItemsModel"]:
        stmt = (
            select(CartItemsModel)
            .options(joinedload(CartItemsModel.book))
            .join(CartsModel, CartsModel.id == CartItemsModel.cart_id)
            .filter(CartsModel.user_id == user_id)
            .limit(limit)
            .offset(offset)
        )
        with SessionLocal() as session:
            return session.scalars(stmt).all()
