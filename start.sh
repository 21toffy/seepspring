#!/bin/bash
python manage.py makemigrations --no-input
python manage.py migrate --no-input
python manage.py collectstatic --no-input
python3 manage.py wait_for_db &&
gunicorn seepspring.wsgi:application -w 5 -b 0.0.0.0:8001 --capture-output --log-level=info
gunicorn seepspring.wsgi:application --bind 0.0.0.0:8001
