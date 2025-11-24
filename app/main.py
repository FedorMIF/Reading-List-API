"""Главный файл FastAPI приложения"""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError

from app.database import engine, Base
from app.routers import items_router, tags_router
from app.config import settings

# Создание таблиц в БД
Base.metadata.create_all(bind=engine)

# Инициализация FastAPI приложения
app = FastAPI(
    title="Reading List API",
    description="API для управления списком чтения (книги и статьи)",
    version="1.0.0",
)

# Подключение роутеров
app.include_router(items_router)
app.include_router(tags_router)


# Обработчики ошибок
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Обработчик ошибок валидации"""
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation error",
            "message": str(exc),
            "details": exc.errors(),
        },
    )


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    """Обработчик ошибок базы данных"""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Database error",
            "message": "An error occurred while processing your request",
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Обработчик общих ошибок"""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc),
        },
    )


# Корневой эндпоинт
@app.get("/")
async def root():
    """Корневой эндпоинт с информацией об API"""
    return {
        "message": "Reading List API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "items": "/items",
            "tags": "/tags",
        },
    }


# Healthcheck
@app.get("/health")
async def health():
    """Проверка работоспособности сервиса"""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True,
    )

