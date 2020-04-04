#!/bin/sh

python3 manage.py collectstatic
python3 manage.py makemigrations
python3 manage.py migrate

uwsgi --show-config