"""Модель элемента списка чтения"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
import enum

from app.database import Base


class ItemKind(str, enum.Enum):
    """Тип материала"""
    BOOK = "book"
    ARTICLE = "article"


class ItemStatus(str, enum.Enum):
    """Статус прочтения"""
    PLANNED = "planned"
    READING = "reading"
    DONE = "done"


class ItemPriority(str, enum.Enum):
    """Приоритет"""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"


class Item(Base):
    """Элемент списка чтения (книга или статья)"""
    
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(500), nullable=False)
    kind = Column(SQLEnum(ItemKind), nullable=False, index=True)
    status = Column(SQLEnum(ItemStatus), default=ItemStatus.PLANNED, nullable=False, index=True)
    priority = Column(SQLEnum(ItemPriority), default=ItemPriority.NORMAL, nullable=False, index=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Связи
    user = relationship("User", back_populates="items")
    tags = relationship("Tag", secondary="item_tags", back_populates="items")

