from fastapi import Response
from sqlalchemy.exc import NoResultFound

from common.schemas import ErrorSchema
from repositories.carts.models import CartItemsModel
from repositories.orders.models import OrdersModel, OrderItemsModel
from repositories.orders.schemas import OrderStatus


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
        return self._order_items_repository.create_order_items(
            order_kwargs, cart_items
        )

    def get_order(self, order_id):
        # Logic to retrieve an order
        return self._orders_repository.get(order_id)

    def update_order(self, order_id, order_data):
        # Logic to update an order
        return self._orders_repository.update(order_id, order_data)

    def delete_order(self, order_id):
        # Logic to delete an order
        return self._orders_repository.delete(order_id)
