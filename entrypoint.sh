#!/bin/sh

python manage.py compilemessages -l ru

python manage.py migrate --noinput

python manage.py collectstatic --noinput

gunicorn config.wsgi:application --bind 0:8000 --log-level debug
