from fastapi import APIRouter
from app.api import todos, storage_routes

router = APIRouter()

router.include_router(todos.router, prefix="/api/todos", tags=["Todos"])
router.include_router(storage_routes.router, prefix="/api/storage", tags=["Storage"])
