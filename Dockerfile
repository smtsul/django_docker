FROM python:3.9-alpine
ENV PYTHONUNBUFFERED 1
WORKDIR /app

# Копируем зависимости проекта и устанавливаем их
COPY orion_express/ /app/
RUN pip install -r requirements.txt

# Команда для запуска Django приложения
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
