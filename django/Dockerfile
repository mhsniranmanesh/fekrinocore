# FROM python:3
# docker build -t ubuntu1604py36
FROM ubuntu:18.04

ARG APP_USER=ubuntu
RUN groupadd -r ${APP_USER} && useradd --no-log-init -r -g ${APP_USER} ${APP_USER}

RUN apt update -y
RUN apt-get update -y
RUN apt-get install -y software-properties-common vim
RUN add-apt-repository ppa:deadsnakes/ppa -y

RUN apt-get install -y build-essential python3.8 python3.8-dev python3-pip python3.8-venv
RUN apt-get install -y git

RUN apt-get update

RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 2

# update pip
RUN python3.8 -m pip install pip --upgrade
RUN python3.8 -m pip install wheel

RUN apt-get install -y gdal-bin \
    libgdal-dev \
    python3-gdal \
    binutils \
    libpq-dev \
    libproj-dev


ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code
COPY ./requirments.txt /code/
RUN pip install -r requirments.txt

COPY . /code/

# uWSGI will listen on this port
EXPOSE 8000

# Add any static environment variables needed by Django or your settings file here:
ENV DJANGO_SETTINGS_MODULE=fekrino.settings

# Call collectstatic (customize the following line with the minimal environment variables needed for manage.py to run):
#RUN python manage.py collectstatic --noinput

# Tell uWSGI where to find your wsgi file (change this):
ENV UWSGI_WSGI_FILE=fekrino/wsgi.py

# Base uWSGI configuration (you shouldn't need to change these):
ENV UWSGI_HTTP=:8000 UWSGI_MASTER=1 UWSGI_HTTP_AUTO_CHUNKED=1 UWSGI_HTTP_KEEPALIVE=1 UWSGI_LAZY_APPS=1 UWSGI_WSGI_ENV_BEHAVIOR=holy

# Number of uWSGI workers and threads per worker (customize as needed):
ENV UWSGI_WORKERS=2 UWSGI_THREADS=4

# uWSGI static file serving configuration (customize or comment out if not needed):
#ENV UWSGI_STATIC_MAP="/static/=/code/static/" UWSGI_STATIC_EXPIRES_URI="/static/.*\.[a-f0-9]{12,}\.(css|js|png|jpg|jpeg|gif|ico|woff|ttf|otf|svg|scss|map|txt) 315360000"

# Deny invalid hosts before they get to Django (uncomment and change to your hostname(s)):
# ENV UWSGI_ROUTE_HOST="^(?!localhost:8000$) break:400"

# Change to a non-root user
USER ${APP_USER}:${APP_USER}

# Uncomment after creating your docker-entrypoint.sh
ENTRYPOINT ["/code/docker-entrypoint.sh"]

# Start uWSGI
CMD ["uwsgi", "--show-config"]


# CMD [ "./run.sh"]
# CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
