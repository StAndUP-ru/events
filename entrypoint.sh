#!/bin/sh

python manage.py compilemessages -l ru

python manage.py migrate --noinput

python manage.py initial_specializations

python manage.py collectstatic --noinput

gunicorn event_app.wsgi:application --bind 0:8000

# gunicorn event_app.wsgi:application --bind 0:8000 \
#     & celery -A event_app worker --loglevel=info \
#     & celery -A event_app beat --loglevel=info \
#     & celery -A event_app flower --loglevel=info
