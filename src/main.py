# Packages
import uvicorn
from fastapi import FastAPI
from apis import apis

app = FastAPI()

for api in apis:
    app.include_router(api)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8545, reload=True)
