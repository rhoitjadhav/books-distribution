# Packages
import uvicorn
from fastapi import FastAPI

from apis import apis
from common.exceptions import add_exception_handlers

app = FastAPI()

# Add exception handlers
add_exception_handlers(app)

for api in apis:
    app.include_router(api, prefix="/api")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8545, reload=True)
