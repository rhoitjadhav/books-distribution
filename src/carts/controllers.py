from fastapi import APIRouter, Response

from carts.services import CartsService
from repositories.books.models import BooksModel
from repositories.carts.models import CartsModel, CartItemsModel
from repositories.carts.schemas import CartItemSchema

router = APIRouter(prefix="/carts")


@router.get("")
def get_cart_items(
    response: Response,
    user_id: str = "75e8b351-f612-4eff-8dfe-6544e73a8df4",  # remove this default value
    page: int = 1,
    page_size: int = 10,
):
    return CartsService(
        response, CartsModel, CartItemsModel, BooksModel
    ).get_cart_items(user_id, page, page_size)


@router.post("")
def add_to_cart(
    response: Response,
    cart_item: CartItemSchema,
    user_id: str = "75e8b351-f612-4eff-8dfe-6544e73a8df4",  # remove this default value
):
    return CartsService(response, CartsModel, CartItemsModel, BooksModel).add_to_cart(
        user_id, cart_item
    )


@router.delete("/{cart_item_id}")
def remove_cart_item(cart_item_id: str, response: Response):
    return CartsService(
        response, CartsModel, CartItemsModel, BooksModel
    ).remove_cart_item(cart_item_id)
