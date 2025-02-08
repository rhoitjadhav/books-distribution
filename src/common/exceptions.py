from fastapi import FastAPI, Request, HTTPException
from sqlalchemy.exc import NoResultFound
from starlette.responses import JSONResponse


async def exception_handler(_: Request, exc: Exception):
    if isinstance(exc, NoResultFound):
        return JSONResponse(status_code=404, content={"error": str(exc)})
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
