"""API роутеры"""
from app.routers.items import router as items_router
from app.routers.tags import router as tags_router

__all__ = ["items_router", "tags_router"]

