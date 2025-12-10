from fastapi import FastAPI, status, HTTPException, APIRouter
from routers.category import category_router


def create_app() -> FastAPI:
    app = FastAPI()

    app.include_router(category_router)

    return app
