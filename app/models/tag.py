"""Модель тега"""
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database import Base


class Tag(Base):
    """Тег для категоризации материалов"""
    
    __tablename__ = "tags"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    
    # Связи
    user = relationship("User", back_populates="tags")
    items = relationship("Item", secondary="item_tags", back_populates="tags")
    
    # Ограничение уникальности имени в рамках пользователя
    __table_args__ = (
        UniqueConstraint("user_id", "name", name="uq_user_tag_name"),
    )

