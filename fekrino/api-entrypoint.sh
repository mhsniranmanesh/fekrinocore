#!/bin/sh

uwsgi --show-config
python3 manage.py collectstatic --noinput
python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput
echo "FUCKKKKK YOU"
