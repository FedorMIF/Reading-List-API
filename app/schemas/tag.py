"""Схемы для Tag"""
from pydantic import BaseModel, ConfigDict


class TagBase(BaseModel):
    """Базовая схема тега"""
    name: str


class TagCreate(TagBase):
    """Схема создания тега"""
    user_id: int


class Tag(TagBase):
    """Полная схема тега"""
    id: int
    user_id: int
    
    model_config = ConfigDict(from_attributes=True)


class TagResponse(BaseModel):
    """Ответ с данными тега"""
    data: Tag


class TagListResponse(BaseModel):
    """Ответ со списком тегов"""
    data: list[Tag]
    total: int

