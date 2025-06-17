# Packages
from fastapi import APIRouter, Response, Depends

# Modules
from auth import get_jwt_sub
from orders.services import OrdersService
from repositories.carts.models import CartItemsModel
from repositories.orders.models import OrdersModel, OrderItemsModel
from repositories.users.models import UsersModel
from repositories.users.schemas import UserInfoSchema

router = APIRouter(prefix="/orders")


@router.get("/{order_id}")
def get_order(
    order_id: str, response: Response, user_id: str = Depends(get_jwt_sub)
):
    return OrdersService(
        response, OrdersModel(), OrderItemsModel, CartItemsModel, UsersModel()
    ).get_order(order_id=order_id, user_id=user_id)


@router.get("")
def list_orders(
    response: Response, page: int = 1, user_id: str = Depends(get_jwt_sub)
):
    return OrdersService(
        response, OrdersModel(), OrderItemsModel, CartItemsModel, UsersModel()
    ).list_orders(user_id=user_id, page=page)


@router.post("/checkout")
def checkout_order(
    response: Response,
    cart_item_ids: list[str],
    user_info: UserInfoSchema,
    user_id: str = Depends(get_jwt_sub),
):
    return OrdersService(
        response, OrdersModel, OrderItemsModel, CartItemsModel, UsersModel()
    ).checkout_order(user_info, cart_item_ids, user_id)
