from fastapi import APIRouter, Response

from orders.services import OrdersService
from repositories.carts.models import CartItemsModel
from repositories.orders.models import OrdersModel, OrderItemsModel


router = APIRouter(prefix="/orders")


@router.get("")
def get_orders(
    response: Response,
    user_id: str = "75e8b351-f612-4eff-8dfe-6544e73a8df4",  # remove this default value
):
    return OrdersService(
        Response(), OrdersModel, OrderItemsModel, CartItemsModel
    ).get_orders()


@router.post("/checkout")
def checkout_order(
    response: Response,
    cart_item_ids: list[str],
    user_id: str = "75e8b351-f612-4eff-8dfe-6544e73a8df4",  # remove this default value
):
    return OrdersService(
        response, OrdersModel, OrderItemsModel, CartItemsModel
    ).checkout_order(user_id, cart_item_ids)
