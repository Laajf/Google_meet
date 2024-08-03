# Используем официальный Python образ версии 3.12 в качестве базового
FROM python:3.12-slim

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y curl && apt-get clean && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry
RUN pip install poetry

# Создаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта
COPY pyproject.toml poetry.lock* ./

# Устанавливаем зависимости через Poetry
RUN poetry install --no-interaction --no-ansi

# Копируем остальной код
COPY . .

# Указываем команду для запуска приложения
CMD ["poetry", "run", "python", "main.py"]
