#!/bin/sh

sleep 5
python3 manage.py collectstatic --noinput
python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput

uwsgi --show-config