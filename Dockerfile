FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/

RUN apt-get update && apt-get install -y \
    libpq-dev gcc supervisor && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    apt-get clean

COPY . /app/

EXPOSE 8000

COPY supervisord.conf /app/supervisord.conf

CMD ["supervisord", "-c", "/app/supervisord.conf"]
