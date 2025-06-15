from fastapi import FastAPI, Request, HTTPException
from starlette.responses import JSONResponse


class NotFoundException(Exception):
    def __init__(self, error_msg: str = "Resource not found"):
        self.status_code = 404
        self.error = error_msg


async def exception_handler(_: Request, exc: Exception):
    if isinstance(exc, NotFoundException):
        return JSONResponse(
            status_code=exc.status_code, content={"error": exc.error}
        )
    elif isinstance(exc, HTTPException):
        return JSONResponse(
            status_code=exc.status_code, content={"error": exc.detail}
        )
    return JSONResponse(
        status_code=500,
        content={"error": "Something went wrong", "detail": str(exc)},
    )


def add_exception_handlers(app: FastAPI):
    app.add_exception_handler(Exception, exception_handler)
