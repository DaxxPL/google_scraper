#!/bin/sh

sleep 5s

python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8000