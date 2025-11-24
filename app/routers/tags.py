"""API endpoints для работы с Tags"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Tag
from app.schemas.tag import TagCreate, TagResponse, TagListResponse


router = APIRouter(prefix="/tags", tags=["tags"])


@router.post("", response_model=TagResponse, status_code=201)
def create_tag(tag: TagCreate, db: Session = Depends(get_db)):
    """Создать новый тег"""
    
    # Проверяем уникальность имени для пользователя
    existing = db.query(Tag).filter(
        Tag.user_id == tag.user_id,
        Tag.name == tag.name
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Tag '{tag.name}' already exists for this user"
        )
    
    db_tag = Tag(user_id=tag.user_id, name=tag.name)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    
    return {"data": db_tag}


@router.get("", response_model=TagListResponse)
def list_tags(
    user_id: Optional[int] = Query(None, description="Фильтр по пользователю"),
    name_contains: Optional[str] = Query(None, description="Поиск по подстроке в имени"),
    db: Session = Depends(get_db),
):
    """Получить список тегов с фильтрацией"""
    
    query = db.query(Tag)
    
    if user_id is not None:
        query = query.filter(Tag.user_id == user_id)
    
    if name_contains:
        query = query.filter(Tag.name.ilike(f"%{name_contains}%"))
    
    tags = query.order_by(Tag.name).all()
    
    return {"data": tags, "total": len(tags)}


@router.get("/{tag_id}", response_model=TagResponse)
def get_tag(tag_id: int, db: Session = Depends(get_db)):
    """Получить тег по ID"""
    
    db_tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not db_tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    
    return {"data": db_tag}


@router.delete("/{tag_id}", status_code=204)
def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    """Удалить тег"""
    
    db_tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not db_tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    
    db.delete(db_tag)
    db.commit()
    
    return None

