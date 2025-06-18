from books.controllers import (
    router as books_router,
    router_admin as books_router_admin,
)
from authors.controllers import router as authors_router
from publishers.controllers import router as publishers_router
from bulk_upload.controllers import router as bulk_upload_router
from carts.controllers import router as carts_router
from orders.controllers import router as orders_router
from users.controllers import router as users_router

apis = [
    users_router,
    books_router,
    carts_router,
    orders_router,
]

admin_only_apis = [
    books_router_admin,
    bulk_upload_router,
    authors_router,
    publishers_router,
]
