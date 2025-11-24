FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/
COPY seed_data.py .
COPY alembic.ini .
COPY alembic/ ./alembic/

RUN mkdir -p /app/data

ENV DATABASE_URL=sqlite:////app/data/reading_list.db
ENV API_HOST=0.0.0.0
ENV API_PORT=8000

EXPOSE 8000

CMD ["python", "-m", "app.main"]

