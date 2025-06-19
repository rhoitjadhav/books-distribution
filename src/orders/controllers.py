# Packages
from fastapi import APIRouter, Depends

# Modules
from auth import get_jwt_sub
from orders.services import OrdersService
from repositories.authors.models import AuthorsModel
from repositories.carts.models import CartItemsModel
from repositories.orders.models import OrdersModel, OrderItemsModel
from repositories.orders.schemas import CheckoutRequestSchema
from repositories.publishers.models import PublishersModel
from repositories.user_addresses.models import UserAddressesModel
from repositories.users.models import UsersModel

router = APIRouter(prefix="/orders")


@router.get("/{order_id}")
def get_order(order_id: str, user_id: str = Depends(get_jwt_sub)):
    return OrdersService(OrdersModel()).get_order(
        order_id=order_id, user_id=user_id
    )


@router.get("")
def list_orders(page: int = 1, user_id: str = Depends(get_jwt_sub)):
    return OrdersService(OrdersModel()).list_orders(user_id=user_id, page=page)


@router.post("/checkout")
def checkout_order(
    crs: CheckoutRequestSchema,
    user_id: str = Depends(get_jwt_sub),
):
    service = OrdersService(
        OrdersModel,
        OrderItemsModel,
        CartItemsModel,
        UsersModel(),
        UserAddressesModel,
        AuthorsModel,
        PublishersModel,
    )
    return service.checkout_order(
        crs.user_info,
        crs.cart_item_ids,
        user_id,
        crs.address_info,
        crs.address_id,
    )
