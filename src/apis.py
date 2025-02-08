from books.controllers import router as books_router
from authors.controllers import router as authors_router
from publishers.controllers import router as publishers_router
from bulk_upload.controllers import router as bulk_upload_router

apis = [books_router, authors_router, publishers_router, bulk_upload_router]
