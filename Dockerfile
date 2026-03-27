FROM python:3.13-slim

WORKDIR /app

RUN pip install poetry && \
    poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --no-interaction

COPY src/ src/

CMD ["uvicorn", "src.notes_manager.main:app", "--host", "0.0.0.0", "--port", "8000"]
