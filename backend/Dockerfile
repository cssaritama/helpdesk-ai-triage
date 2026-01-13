FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir --upgrade pip

COPY pyproject.toml /app/pyproject.toml
RUN pip install --no-cache-dir -e . 

COPY alembic.ini /app/alembic.ini
COPY alembic /app/alembic
COPY app /app/app

EXPOSE 8000

CMD ["bash", "-lc", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
