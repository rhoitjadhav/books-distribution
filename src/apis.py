from books.controllers import router as books_router
from authors.controllers import router as authors_router
from publishers.controllers import router as publishers_router

apis = [books_router, authors_router, publishers_router]
