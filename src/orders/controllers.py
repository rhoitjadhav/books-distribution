from fastapi import APIRouter, Response

from orders.services import OrdersService
from repositories.carts.models import CartItemsModel
from repositories.orders.models import OrdersModel, OrderItemsModel


router = APIRouter(prefix="/orders")


@router.get("/{order_id}")
def get_order(
    order_id: str,
    response: Response,
):
    return OrdersService(
        response, OrdersModel(), OrderItemsModel, CartItemsModel
    ).get_order(order_id=order_id)


@router.get("")
def list_orders(
    response: Response,
    user_id: str = "75e8b351-f612-4eff-8dfe-6544e73a8df4",  # remove this default value
    page: int = 1,
    page_size: int = 10,
):
    return OrdersService(
        response, OrdersModel(), OrderItemsModel, CartItemsModel
    ).list_orders(user_id=user_id, page=page, page_size=page_size)


@router.post("/checkout")
def checkout_order(
    response: Response,
    cart_item_ids: list[str],
    user_id: str = "75e8b351-f612-4eff-8dfe-6544e73a8df4",  # remove this default value
):
    return OrdersService(
        response, OrdersModel, OrderItemsModel, CartItemsModel
    ).checkout_order(user_id, cart_item_ids)
