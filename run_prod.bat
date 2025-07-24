@echo off
echo Starting Django in Production Mode...
set DJANGO_DEBUG=False
python manage.py runserver 