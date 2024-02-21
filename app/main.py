import uvicorn
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from router import menu, user, base, auth

app = FastAPI(docs_url=None, redoc_url=None)
app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent.absolute() / "public/static"),
    name="static",
)

app.include_router(auth.router)
app.include_router(base.router)
app.include_router(menu.router)
app.include_router(user.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)