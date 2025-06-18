from fastapi import APIRouter, Depends

from auth import get_jwt_sub
from carts.services import CartsService
from repositories.books.models import BooksModel
from repositories.carts.models import CartsModel, CartItemsModel
from repositories.carts.schemas import CartItemSchema

router = APIRouter(prefix="/carts")


@router.get("")
def get_cart_items(
    page: int = 1,
    user_id: str = Depends(get_jwt_sub),
):
    return CartsService(CartsModel, CartItemsModel, BooksModel).get_cart_items(
        user_id, page
    )


@router.post("")
def add_to_cart(
    cart_item: CartItemSchema,
    user_id: str = Depends(get_jwt_sub),
):
    return CartsService(CartsModel, CartItemsModel, BooksModel).add_to_cart(
        user_id, cart_item
    )


@router.put("/{cart_item_id}")
def update_cart_item(
    cart_item_id: str,
    cart_item: CartItemSchema,
    _: str = Depends(get_jwt_sub),
):
    return CartsService(
        CartsModel, CartItemsModel, BooksModel
    ).update_cart_item(cart_item_id, cart_item)


@router.delete("/{cart_item_id}")
def remove_cart_item(cart_item_id: str, _: str = Depends(get_jwt_sub)):
    return CartsService(
        CartsModel, CartItemsModel, BooksModel
    ).remove_cart_item(cart_item_id)
