#!/bin/bash
# Скрипт для очистки и пересоздания базы данных с seed данными

echo "[INFO] Удаление существующей базы данных..."

if [ -f "reading_list.db" ]; then
    rm reading_list.db
    echo "[SUCCESS] База данных удалена"
else
    echo "[INFO] База данных не найдена"
fi

echo ""
echo "[INFO] Создание новой базы данных и загрузка seed данных..."
echo ""

source venv/bin/activate 2>/dev/null || true
python seed_data.py

echo ""
echo "[SUCCESS] База данных пересоздана!"

