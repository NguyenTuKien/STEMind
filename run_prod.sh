#!/bin/bash
echo "Starting Django in Production Mode..."
export DJANGO_DEBUG=False
python manage.py runserver 