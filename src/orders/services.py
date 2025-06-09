from fastapi import Response
from sqlalchemy.exc import NoResultFound

from common.helper import get_limit_offset, to_dict
from common.schemas import ErrorSchema
from repositories.carts.models import CartItemsModel
from repositories.orders.models import OrdersModel, OrderItemsModel
from repositories.orders.schemas import (
    OrderStatus,
    OrdersSchema,
    OrderItemsSchema,
)


class OrdersService:
    def __init__(
        self,
        response: Response,
        orders_repository: OrdersModel,
        order_items_repository: OrderItemsModel,
        cart_items_repository: CartItemsModel,
    ):
        self._orders_repository = orders_repository
        self._order_items_repository = orders_repository
        self._order_items_repository = order_items_repository
        self._cart_items_repository = cart_items_repository
        self._response = response

    def checkout_order(self, user_id: str, cart_item_ids: list[str]):
        if not cart_item_ids:
            self._response.status_code = 400
            return ErrorSchema(message="Cart item IDs cannot be empty")

        limit = len(cart_item_ids)
        offset = 0
        filters = [
            CartItemsModel.cart_item_id.in_(cart_item_ids),
        ]
        cart_items = self._cart_items_repository.get_cart_items(
            user_id, limit, offset, *filters
        )
        if not cart_items:
            raise NoResultFound(
                "Cart items not found or empty. "
                "Please add items to your cart before checking out."
            )

        total = sum(item.book.price * item.quantity for item in cart_items)
        order_kwargs = dict(
            order_id=self._orders_repository.generate_order_id(),
            user_id=user_id,
            total_amount=total,
            status=OrderStatus.CONFIRMED,
        )
        order, _ = self._order_items_repository.create_order_items(
            order_kwargs, cart_items
        )

        self._cart_items_repository.delete(
            CartItemsModel.cart_item_id.in_(cart_item_ids)
        )
        return order

    def list_orders(self, user_id: str, page: int, page_size: int):
        limit, offset = get_limit_offset(page, page_size)
        orders = self._orders_repository.get_all(
            limit, offset, user_id=user_id
        )
        return [
            OrdersSchema.model_validate(to_dict(order)) for order in orders
        ]

    def get_order(self, order_id: str):
        order_items = self._order_items_repository.get_order_items(order_id)
        return [
            OrderItemsSchema.model_validate(to_dict(item))
            for item in order_items
        ]
