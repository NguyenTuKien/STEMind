#!/bin/bash
echo "Starting Django in Development Mode..."
export DJANGO_DEBUG=True
python manage.py runserver 