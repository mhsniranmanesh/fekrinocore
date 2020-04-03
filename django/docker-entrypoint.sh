#!/bin/sh

python3.8 manage.py collectstatic --noinput
python3.8 manage.py makemigrations --noinput
python3.8 manage.py migrate --noinput