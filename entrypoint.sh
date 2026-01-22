#!/bin/bash
export PYTHONPATH=./vendor
echo "Starting Django Application"
python3 manage.py migrate --noinput
echo "creating superuser"
python3 manage.py createsuperuser --noinput
echo "Starting Gunicorn"
python3 -m gunicorn --workers 2 python_apps_django.wsgi --bind 0.0.0.0:8000