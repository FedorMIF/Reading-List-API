#!/bin/bash
# Скрипт запуска Reading List API

echo "[INFO] Запуск Reading List API..."

# Активация виртуального окружения
if [ ! -d "venv" ]; then
    echo "[ERROR] Виртуальное окружение не найдено. Запустите: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

source venv/bin/activate

# Проверка зависимостей
if ! python -c "import fastapi" 2>/dev/null; then
    echo "[ERROR] Зависимости не установлены. Запустите: pip install -r requirements.txt"
    exit 1
fi

# Проверка наличия БД
if [ ! -f "reading_list.db" ]; then
    echo "[WARNING] База данных не найдена. Загружаем seed данные..."
    python seed_data.py
fi

echo "[SUCCESS] Запуск сервера на http://localhost:8000"
echo "[INFO] Документация: http://localhost:8000/docs"
echo ""

# Запуск сервера
python -m app.main

