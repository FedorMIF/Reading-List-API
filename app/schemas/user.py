"""Схемы для User"""
from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
    """Базовая схема пользователя"""
    email: EmailStr
    display_name: str


class UserCreate(UserBase):
    """Схема создания пользователя"""
    pass


class User(UserBase):
    """Полная схема пользователя"""
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class UserResponse(BaseModel):
    """Ответ с данными пользователя"""
    data: User

