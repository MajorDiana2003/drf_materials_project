FROM python:3.12-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Установка рабочей директории внутри контейнера
WORKDIR /app

# Отключение кэширования байт-кода Python и включение моментального вывода логов
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Копирование списка зависимостей
COPY requirements.txt .


RUN pip install --no-cache-dir --upgrade pip


RUN pip install --no-cache-dir -r requirements.txt

# Копирование всего кода проекта в контейнер
COPY . .

# Команда по умолчанию для запуска приложения
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

