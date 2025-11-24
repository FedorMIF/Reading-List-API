"""Скрипт для загрузки тестовых данных в БД"""
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.database import SessionLocal, engine, Base
from app.models import User, Item, Tag
from app.models.item import ItemKind, ItemStatus, ItemPriority


def create_seed_data():
    """Создать тестовые данные"""
    
    # Создаём таблицы если их нет
    Base.metadata.create_all(bind=engine)
    
    db: Session = SessionLocal()
    
    try:
        # Проверяем, есть ли уже данные
        if db.query(User).count() > 0:
            print("[ERROR] База данных уже содержит данные. Очистите её перед загрузкой seed данных.")
            return
        
        print("[INFO] Создание seed данных...")
        
        # Создаём пользователей
        user1 = User(
            email="alice@example.com",
            display_name="Alice Reader",
            created_at=datetime.utcnow() - timedelta(days=30)
        )
        user2 = User(
            email="bob@example.com",
            display_name="Bob Bookworm",
            created_at=datetime.utcnow() - timedelta(days=20)
        )
        
        db.add(user1)
        db.add(user2)
        db.commit()
        db.refresh(user1)
        db.refresh(user2)
        
        print(f"[SUCCESS] Создано 2 пользователя: {user1.display_name}, {user2.display_name}")
        
        # Создаём теги для пользователя 1
        tags_user1 = [
            Tag(user_id=user1.id, name="python"),
            Tag(user_id=user1.id, name="sci-fi"),
            Tag(user_id=user1.id, name="technical"),
            Tag(user_id=user1.id, name="fantasy"),
        ]
        
        # Создаём теги для пользователя 2
        tags_user2 = [
            Tag(user_id=user2.id, name="history"),
            Tag(user_id=user2.id, name="biography"),
            Tag(user_id=user2.id, name="programming"),
        ]
        
        for tag in tags_user1 + tags_user2:
            db.add(tag)
        
        db.commit()
        
        for tag in tags_user1 + tags_user2:
            db.refresh(tag)
        
        print(f"[SUCCESS] Создано {len(tags_user1) + len(tags_user2)} тегов")
        
        # Создаём элементы для пользователя 1
        items_user1 = [
            Item(
                user_id=user1.id,
                title="Clean Code: A Handbook of Agile Software Craftsmanship",
                kind=ItemKind.BOOK,
                status=ItemStatus.DONE,
                priority=ItemPriority.HIGH,
                notes="Отличная книга о чистом коде. Много практических примеров.",
                created_at=datetime.utcnow() - timedelta(days=25),
                updated_at=datetime.utcnow() - timedelta(days=10),
            ),
            Item(
                user_id=user1.id,
                title="The Hitchhiker's Guide to the Galaxy",
                kind=ItemKind.BOOK,
                status=ItemStatus.READING,
                priority=ItemPriority.NORMAL,
                notes="Забавная научная фантастика",
                created_at=datetime.utcnow() - timedelta(days=15),
                updated_at=datetime.utcnow() - timedelta(days=3),
            ),
            Item(
                user_id=user1.id,
                title="Understanding Python Decorators",
                kind=ItemKind.ARTICLE,
                status=ItemStatus.DONE,
                priority=ItemPriority.HIGH,
                notes="Хорошее объяснение декораторов",
                created_at=datetime.utcnow() - timedelta(days=10),
                updated_at=datetime.utcnow() - timedelta(days=9),
            ),
            Item(
                user_id=user1.id,
                title="Dune",
                kind=ItemKind.BOOK,
                status=ItemStatus.PLANNED,
                priority=ItemPriority.NORMAL,
                notes="Классика научной фантастики",
                created_at=datetime.utcnow() - timedelta(days=5),
                updated_at=datetime.utcnow() - timedelta(days=5),
            ),
            Item(
                user_id=user1.id,
                title="FastAPI Best Practices",
                kind=ItemKind.ARTICLE,
                status=ItemStatus.READING,
                priority=ItemPriority.HIGH,
                notes="",
                created_at=datetime.utcnow() - timedelta(days=2),
                updated_at=datetime.utcnow() - timedelta(days=1),
            ),
        ]
        
        # Создаём элементы для пользователя 2
        items_user2 = [
            Item(
                user_id=user2.id,
                title="Sapiens: A Brief History of Humankind",
                kind=ItemKind.BOOK,
                status=ItemStatus.READING,
                priority=ItemPriority.HIGH,
                notes="Увлекательная история человечества",
                created_at=datetime.utcnow() - timedelta(days=18),
                updated_at=datetime.utcnow() - timedelta(days=2),
            ),
            Item(
                user_id=user2.id,
                title="The Pragmatic Programmer",
                kind=ItemKind.BOOK,
                status=ItemStatus.PLANNED,
                priority=ItemPriority.NORMAL,
                notes="",
                created_at=datetime.utcnow() - timedelta(days=12),
                updated_at=datetime.utcnow() - timedelta(days=12),
            ),
            Item(
                user_id=user2.id,
                title="Introduction to Machine Learning",
                kind=ItemKind.ARTICLE,
                status=ItemStatus.DONE,
                priority=ItemPriority.LOW,
                notes="Базовое введение",
                created_at=datetime.utcnow() - timedelta(days=7),
                updated_at=datetime.utcnow() - timedelta(days=6),
            ),
        ]
        
        # Добавляем элементы с тегами
        # User 1 items
        items_user1[0].tags = [tags_user1[2]]  # Clean Code -> technical
        items_user1[1].tags = [tags_user1[1]]  # Hitchhiker -> sci-fi
        items_user1[2].tags = [tags_user1[0], tags_user1[2]]  # Python article -> python, technical
        items_user1[3].tags = [tags_user1[1], tags_user1[3]]  # Dune -> sci-fi, fantasy
        items_user1[4].tags = [tags_user1[0], tags_user1[2]]  # FastAPI -> python, technical
        
        # User 2 items
        items_user2[0].tags = [tags_user2[0]]  # Sapiens -> history
        items_user2[1].tags = [tags_user2[2]]  # Pragmatic Programmer -> programming
        items_user2[2].tags = [tags_user2[2]]  # ML article -> programming
        
        for item in items_user1 + items_user2:
            db.add(item)
        
        db.commit()
        
        print(f"[SUCCESS] Создано {len(items_user1) + len(items_user2)} элементов списка чтения")
        print("\n[SUCCESS] Seed данные успешно загружены!")
        print("\n[INFO] Статистика:")
        print(f"   - Пользователей: {db.query(User).count()}")
        print(f"   - Элементов: {db.query(Item).count()}")
        print(f"   - Тегов: {db.query(Tag).count()}")
        
    except Exception as e:
        print(f"[ERROR] Ошибка при создании seed данных: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    create_seed_data()

