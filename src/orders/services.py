# Packages
from typing import Optional

from sqlalchemy.orm import load_only

# Modules
from common.exceptions import NotFoundException
from common.helper import get_limit_offset, to_dict
from repositories.authors.models import AuthorsModel
from repositories.books.schemas import BookMetaDataSchema
from repositories.carts.models import CartItemsModel
from repositories.orders.models import OrdersModel, OrderItemsModel
from repositories.orders.schemas import (
    OrderStatus,
    OrdersSchema,
    OrderItemsSchema,
    OrderDetailsSchema,
)
from repositories.publishers.models import PublishersModel
from repositories.user_addresses.models import UserAddressesModel
from repositories.user_addresses.schemas import (
    AddressRequestSchema,
    AddressSchema,
)
from repositories.users.models import UsersModel
from repositories.users.schemas import UserInfoSchema, UsersSchema


class OrdersService:
    def __init__(
        self,
        orders_repository: OrdersModel,
        order_items_repository: OrderItemsModel = None,
        cart_items_repository: CartItemsModel = None,
        users_repository: UsersModel = None,
        ua_repository: UserAddressesModel = None,
        authors_repository: AuthorsModel = None,
        publishers_repository: PublishersModel = None,
    ):
        self._orders_repository = orders_repository
        self._order_items_repository = orders_repository
        self._order_items_repository = order_items_repository
        self._cart_items_repository = cart_items_repository
        self._users_repository = users_repository
        self._ua_repository = ua_repository
        self._authors_repository = authors_repository
        self._publishers_repository = publishers_repository

    def list_orders(self, user_id: str, page: int, page_size: int = 10):
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

        return OrderDetailsSchema(
            order_id=order.order_id,
            order_amount=order.total_amount,
            status=order.status,
            address_meta_data=order.address_meta_data,
            user_meta_data=order.user_meta_data,
            items=[
                OrderItemsSchema.model_validate(to_dict(item))
                for item in order.items
            ],
        )

    def checkout_order(
        self,
        user_info: UserInfoSchema,
        cart_item_ids: list[str],
        user_id: Optional[str],
        address_info: Optional[AddressRequestSchema] = None,
        address_id: Optional[str] = None,
    ):
        if not (address_id or address_info):
            raise NotFoundException(
                "Address ID or address info are required for checkout."
            )

        if not cart_item_ids:
            raise NotFoundException("Cart item IDs cannot be empty")

        if not user_id:
            user = UsersSchema.model_validate(
                self._users_repository.create_or_get(**user_info.dict())
            )
            user_id = user.user_id

        if not address_info:
            address = self._ua_repository.get(address_id=address_id)
            if not address:
                raise NotFoundException(
                    "Address not found. Please provide a valid address ID"
                )
            address_info = AddressRequestSchema.model_validate(
                to_dict(address)
            )

        if not address_id:
            address_id = AddressSchema.model_validate(
                self._ua_repository.create(
                    user_id=user_id, **address_info.dict()
                )
            ).address_id

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
        order_id = self._orders_repository.generate_order_id()
        order_kwargs = dict(
            order_id=order_id,
            user_id=user_id,
            total_amount=total,
            status=OrderStatus.CONFIRMED,
            user_meta_data=user_info.dict(),
            address_id=address_id,
            address_meta_data=address_info.dict(),
        )

        order_items = []
        for item in cart_items:
            book = item.book
            book_media_data = book.media_data
            author = self._authors_repository.get(
                options=[load_only(AuthorsModel.name)],
                author_id=book.author_id,
            )
            publisher = self._publishers_repository.get(
                options=[load_only(PublishersModel.name)],
                publisher_id=book.publisher_id,
            )
            book_meta_data = BookMetaDataSchema(
                book_id=item.book_id,
                book_title=book.book_title,
                author_name=author.name if author else "",
                publisher_name=publisher.name if publisher else "",
                media=book_media_data[0] if book_media_data else "",
            )
            order_items.append(
                OrderItemsSchema(
                    order_id=order_id,
                    book_id=item.book_id,
                    book_meta_data=book_meta_data.model_dump(),
                    quantity=item.quantity,
                    total_amount=item.book.price * item.quantity,
                ).model_dump()
            )

        order, _ = self._order_items_repository.create_order_items(
            order_kwargs, order_items
        )

        # self._cart_items_repository.delete(
        #     CartItemsModel.cart_item_id.in_(cart_item_ids)
        # )
        return OrdersSchema.model_validate(order)
