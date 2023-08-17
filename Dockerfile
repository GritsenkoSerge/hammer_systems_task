FROM python:3.11-slim

ENV APP_HOME=/app

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install gettext libpq-dev gcc -y

RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR $APP_HOME

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE config.settings

# Create a user to avoid running containers as root in production
RUN addgroup --system backend_user \
    && adduser --system --ingroup backend_user backend_user

COPY . .
RUN mkdir static \
    && chown -R backend_user:backend_user $APP_HOME

# change user
USER backend_user

# This script will run before every command executed in the container
RUN  sed -i 's/\r$//' ./entrypoint.sh && chmod +x ./entrypoint.sh
ENTRYPOINT  ["./entrypoint.sh"]
