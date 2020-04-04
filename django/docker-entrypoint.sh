#!/bin/sh

pythone manage.py collectstatic
python3 manage.py makemigrations
python3 manage.py migrate