# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей
COPY pyproject.toml poetry.lock* ./

# Устанавливаем Poetry
RUN pip install poetry

# Устанавливаем зависимости
RUN poetry install --no-dev

# Копируем остальной код приложения
COPY . .

# Команда для запуска приложения
CMD ["poetry", "run", "uvicorn", "java_luchshe.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
