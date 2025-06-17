from common.exceptions import NotFoundException, ConflictException
from common.helper import get_limit_offset, to_dict
from repositories.books.models import BooksModel
from repositories.carts.models import CartsModel, CartItemsModel
from repositories.carts.schemas import (
    CartItemSchema,
    CartSchema,
    CartItemsDetailSchema,
    CartItemDeleteSchema,
    CartItemResponseSchema,
)


class CartsService:
    def __init__(
        self,
        carts_repository: CartsModel,
        cart_items_repository: CartItemsModel,
        books_repository: BooksModel,
    ):
        self._carts_repository = carts_repository
        self._cart_items_repository = cart_items_repository
        self._books_repository = books_repository

    def get_cart_items(
        self, user_id: str, page: int, page_size: int = 10
    ) -> list[CartItemsDetailSchema]:
        limit, offset = get_limit_offset(page, page_size)
        cart_items = self._cart_items_repository.get_cart_items(
            user_id=user_id, limit=limit, offset=offset
        )

        result = []
        for item in cart_items:
            _item = to_dict(item)
            _item["book"] = to_dict(item.book)
            result.append(CartItemsDetailSchema.model_validate(_item))

        return result

    def add_to_cart(self, user_id: str, cart_item: CartItemSchema) -> dict:
        book = self._books_repository.get_by_pk(cart_item.book_id)
        if not book:
            raise NotFoundException("Book not found")

        cart = self._carts_repository.get(user_id=user_id)
        if not cart:
            cart = CartSchema(**self._carts_repository.create(user_id=user_id))

        # Check if book is already in the cart
        existing_item = self._cart_items_repository.get(
            cart_id=cart.cart_id, book_id=cart_item.book_id
        )
        if existing_item:
            raise ConflictException("Book already in cart")

        return CartItemResponseSchema.model_validate(
            self._cart_items_repository.create(
                cart_id=cart.cart_id,
                **cart_item.model_dump(),
            )
        )

    def update_cart_item(self, cart_item_id: str, cart_item: CartItemSchema):
        return self._cart_items_repository.update(
            cart_item_id, **cart_item.model_dump()
        )

    def remove_cart_item(self, cart_item_id: str):
        cart_item = self._cart_items_repository.get(id=cart_item_id)
        if not cart_item:
            raise NotFoundException("Cart item not found")

        cart_item = self._cart_items_repository.delete(id=cart_item_id)
        return CartItemDeleteSchema(cart_item_id=cart_item["id"])
