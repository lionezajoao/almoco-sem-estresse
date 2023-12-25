import uvicorn
from fastapi import FastAPI

from api import lib_routes
from api import user_routes

app = FastAPI()
app.include_router(lib_routes.router)
# app.include_router(user_routes.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)