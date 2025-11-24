"""Схемы для Item"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from enum import Enum

from app.schemas.tag import Tag


class ItemKind(str, Enum):
    """Тип материала"""
    BOOK = "book"
    ARTICLE = "article"


class ItemStatus(str, Enum):
    """Статус прочтения"""
    PLANNED = "planned"
    READING = "reading"
    DONE = "done"


class ItemPriority(str, Enum):
    """Приоритет"""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"


class ItemBase(BaseModel):
    """Базовая схема элемента"""
    title: str
    kind: ItemKind
    status: ItemStatus = ItemStatus.PLANNED
    priority: ItemPriority = ItemPriority.NORMAL
    notes: Optional[str] = None


class ItemCreate(ItemBase):
    """Схема создания элемента"""
    user_id: int
    tag_ids: Optional[list[int]] = None


class ItemUpdate(BaseModel):
    """Схема обновления элемента"""
    title: Optional[str] = None
    kind: Optional[ItemKind] = None
    status: Optional[ItemStatus] = None
    priority: Optional[ItemPriority] = None
    notes: Optional[str] = None


class Item(ItemBase):
    """Полная схема элемента"""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    tags: list[Tag] = []
    
    model_config = ConfigDict(from_attributes=True)


class ItemResponse(BaseModel):
    """Ответ с данными элемента"""
    data: Item


class ItemListResponse(BaseModel):
    """Ответ со списком элементов"""
    data: list[Item]
    total: int
    limit: int
    offset: int


class ItemTagUpdate(BaseModel):
    """Схема для добавления/удаления тегов"""
    tag_ids: list[int]

