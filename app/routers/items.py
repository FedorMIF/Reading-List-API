"""API endpoints для работы с Items"""
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Item, Tag
from app.schemas.item import (
    ItemCreate,
    ItemUpdate,
    ItemResponse,
    ItemListResponse,
    ItemKind,
    ItemStatus,
    ItemPriority,
    ItemTagUpdate,
)


router = APIRouter(prefix="/items", tags=["items"])


@router.post("", response_model=ItemResponse, status_code=201)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    """Создать новый элемент списка чтения"""
    
    # Создаём элемент
    db_item = Item(
        user_id=item.user_id,
        title=item.title,
        kind=item.kind,
        status=item.status,
        priority=item.priority,
        notes=item.notes,
    )
    
    # Добавляем теги если указаны
    if item.tag_ids:
        tags = db.query(Tag).filter(
            Tag.id.in_(item.tag_ids),
            Tag.user_id == item.user_id
        ).all()
        db_item.tags = tags
    
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    
    return {"data": db_item}


@router.get("/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    """Получить элемент по ID"""
    
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return {"data": db_item}


@router.get("", response_model=ItemListResponse)
def list_items(
    user_id: Optional[int] = Query(None, description="Фильтр по пользователю"),
    status: Optional[ItemStatus] = Query(None, description="Фильтр по статусу"),
    kind: Optional[ItemKind] = Query(None, description="Фильтр по типу"),
    priority: Optional[ItemPriority] = Query(None, description="Фильтр по приоритету"),
    tag_ids: Optional[str] = Query(None, description="Фильтр по тегам (через запятую, любой из)"),
    title_contains: Optional[str] = Query(None, description="Поиск по подстроке в названии"),
    created_after: Optional[datetime] = Query(None, description="Создано после (ISO datetime)"),
    created_before: Optional[datetime] = Query(None, description="Создано до (ISO datetime)"),
    sort_by: str = Query("created_at", regex="^(created_at|updated_at|priority)$", description="Поле сортировки"),
    sort_order: str = Query("desc", regex="^(asc|desc)$", description="Порядок сортировки"),
    limit: int = Query(50, ge=1, le=100, description="Количество записей"),
    offset: int = Query(0, ge=0, description="Смещение"),
    db: Session = Depends(get_db),
):
    """Получить список элементов с фильтрацией, пагинацией и сортировкой"""
    
    query = db.query(Item)
    
    # Применяем фильтры
    if user_id is not None:
        query = query.filter(Item.user_id == user_id)
    
    if status:
        query = query.filter(Item.status == status)
    
    if kind:
        query = query.filter(Item.kind == kind)
    
    if priority:
        query = query.filter(Item.priority == priority)
    
    if tag_ids:
        tag_id_list = [int(tid.strip()) for tid in tag_ids.split(",")]
        query = query.join(Item.tags).filter(Tag.id.in_(tag_id_list))
    
    if title_contains:
        query = query.filter(Item.title.ilike(f"%{title_contains}%"))
    
    if created_after:
        query = query.filter(Item.created_at >= created_after)
    
    if created_before:
        query = query.filter(Item.created_at <= created_before)
    
    # Подсчёт общего количества (до пагинации)
    total = query.count()
    
    # Сортировка
    order_column = getattr(Item, sort_by)
    if sort_order == "desc":
        order_column = order_column.desc()
    else:
        order_column = order_column.asc()
    
    query = query.order_by(order_column)
    
    # Пагинация
    items = query.offset(offset).limit(limit).all()
    
    return {
        "data": items,
        "total": total,
        "limit": limit,
        "offset": offset,
    }


@router.patch("/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, item_update: ItemUpdate, db: Session = Depends(get_db)):
    """Обновить элемент"""
    
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Обновляем только переданные поля
    update_data = item_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_item, field, value)
    
    db_item.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_item)
    
    return {"data": db_item}


@router.delete("/{item_id}", status_code=204)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    """Удалить элемент"""
    
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    db.delete(db_item)
    db.commit()
    
    return None


@router.post("/{item_id}/tags", response_model=ItemResponse)
def add_tags_to_item(item_id: int, tag_update: ItemTagUpdate, db: Session = Depends(get_db)):
    """Добавить теги к элементу"""
    
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Получаем теги пользователя
    tags = db.query(Tag).filter(
        Tag.id.in_(tag_update.tag_ids),
        Tag.user_id == db_item.user_id
    ).all()
    
    if len(tags) != len(tag_update.tag_ids):
        raise HTTPException(status_code=400, detail="Some tags not found or don't belong to user")
    
    # Добавляем теги (SQLAlchemy автоматически избегает дубликатов)
    for tag in tags:
        if tag not in db_item.tags:
            db_item.tags.append(tag)
    
    db_item.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_item)
    
    return {"data": db_item}


@router.delete("/{item_id}/tags", response_model=ItemResponse)
def remove_tags_from_item(item_id: int, tag_update: ItemTagUpdate, db: Session = Depends(get_db)):
    """Удалить теги из элемента"""
    
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Удаляем указанные теги
    db_item.tags = [tag for tag in db_item.tags if tag.id not in tag_update.tag_ids]
    
    db_item.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_item)
    
    return {"data": db_item}

