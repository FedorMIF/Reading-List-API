#!/bin/bash
# Примеры запросов к Reading List API
# Убедитесь, что сервер запущен: ./run.sh

BASE_URL="http://localhost:8000"

echo "Reading List API - Примеры запросов"
echo "========================================"
echo ""

# Healthcheck
echo "1. Healthcheck:"
curl -s "$BASE_URL/health" | python3 -m json.tool
echo ""
echo "---"
echo ""

# Список всех элементов
echo "2. Все элементы (первые 3):"
curl -s "$BASE_URL/items?limit=3" | python3 -m json.tool
echo ""
echo "---"
echo ""

# Фильтрация по статусу
echo "3. Элементы со статусом 'reading':"
curl -s "$BASE_URL/items?status=reading" | python3 -m json.tool
echo ""
echo "---"
echo ""

# Фильтрация по пользователю
echo "4. Элементы пользователя 1:"
curl -s "$BASE_URL/items?user_id=1&limit=2" | python3 -m json.tool
echo ""
echo "---"
echo ""

# Поиск по названию
echo "5. Поиск по слову 'Python':"
curl -s "$BASE_URL/items?title_contains=Python" | python3 -m json.tool
echo ""
echo "---"
echo ""

# Сортировка по приоритету
echo "6. Сортировка по приоритету (высокий → низкий):"
curl -s "$BASE_URL/items?sort_by=priority&sort_order=desc&limit=3" | python3 -m json.tool
echo ""
echo "---"
echo ""

# Список тегов
echo "7. Все теги:"
curl -s "$BASE_URL/tags" | python3 -m json.tool
echo ""
echo "---"
echo ""

# Получение конкретного элемента
echo "8. Получить элемент #1:"
curl -s "$BASE_URL/items/1" | python3 -m json.tool
echo ""
echo "---"
echo ""

# Создание нового элемента
echo "9. Создание нового элемента:"
curl -s -X POST "$BASE_URL/items" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "title": "Design Patterns: Elements of Reusable Object-Oriented Software",
    "kind": "book",
    "status": "planned",
    "priority": "high",
    "notes": "Классика ООП",
    "tag_ids": [1, 3]
  }' | python3 -m json.tool
echo ""
echo "---"
echo ""

# Обновление элемента
echo "10. Обновление элемента #1 (изменение статуса):"
curl -s -X PATCH "$BASE_URL/items/1" \
  -H "Content-Type: application/json" \
  -d '{"status": "reading"}' | python3 -m json.tool
echo ""
echo "---"
echo ""

# Создание тега
echo "11. Создание нового тега:"
curl -s -X POST "$BASE_URL/tags" \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "name": "typescript"}' | python3 -m json.tool
echo ""
echo "---"
echo ""

echo "[SUCCESS] Все примеры выполнены!"
echo ""
echo "[INFO] Для интерактивной документации откройте: $BASE_URL/docs"

