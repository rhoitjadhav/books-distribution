# Packages
from typing import Optional

from fastapi import Response

# Modules
from common.exceptions import NotFoundException
from common.helper import get_limit_offset, to_dict
from common.schemas import ErrorSchema
from repositories.carts.models import CartItemsModel
from repositories.orders.models import OrdersModel, OrderItemsModel
from repositories.orders.schemas import (
    OrderStatus,
    OrdersSchema,
    OrderItemsSchema,
)
from repositories.users.models import UsersModel
from repositories.users.schemas import UserInfoSchema, UsersSchema


class OrdersService:
    def __init__(
        self,
        response: Response,
        orders_repository: OrdersModel,
        order_items_repository: OrderItemsModel,
        cart_items_repository: CartItemsModel,
        users_repository: UsersModel,
    ):
        self._orders_repository = orders_repository
        self._order_items_repository = orders_repository
        self._order_items_repository = order_items_repository
        self._cart_items_repository = cart_items_repository
        self._users_repository = users_repository
        self._response = response

    def list_orders(self, user_id: str, page: int, page_size: int):
        limit, offset = get_limit_offset(page, page_size)
        orders = self._orders_repository.get_all(
            limit, offset, user_id=user_id
        )
        return [
            OrdersSchema.model_validate(to_dict(order)) for order in orders
        ]

    def get_order(self, order_id: str, user_id: str):
        order = self._orders_repository.get_order_with_items(order_id, user_id)
        if not order:
            raise NotFoundException(
                "Order not found or does not belong to the user"
            )
        return [
            OrderItemsSchema.model_validate(to_dict(item))
            for item in order.items
        ]

    def checkout_order(
        self,
        user_info: UserInfoSchema,
        cart_item_ids: list[str],
        user_id: Optional[str],
    ):
        if not cart_item_ids:
            self._response.status_code = 400
            return ErrorSchema(message="Cart item IDs cannot be empty")

        if not user_id:
            user = UsersSchema.model_validate(
                self._users_repository.create_or_get(**user_info.dict())
            )
            user_id = user.user_id

        filters = [
            CartItemsModel.cart_item_id.in_(cart_item_ids),
        ]
        cart_items = self._cart_items_repository.get_cart_items(
            user_id, len(cart_item_ids), 0, *filters
        )
        if not cart_items:
            raise NotFoundException(
                "Cart items not found or empty. "
                "Please add items to your cart before checking out."
            )

        total = sum(item.book.price * item.quantity for item in cart_items)
        order_kwargs = dict(
            order_id=self._orders_repository.generate_order_id(),
            user_id=user_id,
            total_amount=total,
            status=OrderStatus.CONFIRMED,
            user_meta_data=user_info.dict(),
        )
        order, _ = self._order_items_repository.create_order_items(
            order_kwargs, cart_items
        )

        self._cart_items_repository.delete(
            CartItemsModel.cart_item_id.in_(cart_item_ids)
        )
        return order
