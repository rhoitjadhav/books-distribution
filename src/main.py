# Packages
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from apis import apis
from common.exceptions import add_exception_handlers

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add exception handlers
add_exception_handlers(app)

for api in apis:
    app.include_router(api)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8545, reload=True)
