#!/bin/bash
export PYTHONPATH=./vendor
python3 manage.py migrate --noinput
python3 manage.py createsuperuser --noinput
python3 -m gunicorn --workers 2 python_apps_django.wsgi --bind 0.0.0.0:8000