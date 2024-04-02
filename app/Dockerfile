# Используйте официальный образ Python
FROM python:3.10.12

# Установите рабочую директорию в контейнере
WORKDIR /app

# Копируйте текущий каталог в рабочую директорию в контейнере
COPY . .

# Установите зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Установите необходимые пакеты для ODBC
RUN apt-get update  && apt-get install -y unixodbc-dev

RUN chmod a+x ./docker/*.sh

# Команда для запуска приложения Python
CMD ["gunicorn", "app.main:app", "-w", "4", "--worker-class","uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]