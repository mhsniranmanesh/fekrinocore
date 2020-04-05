FROM ubuntu:18.04

ARG APP_USER=ubuntu

RUN adduser ${APP_USER}
RUN usermod -aG sudo ${APP_USER}

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
RUN python3 -m pip install pip --upgrade
RUN python3 -m pip install wheel

RUN apt-get install -y gdal-bin \
    libgdal-dev \
    python3-gdal \
    binutils \
    libpq-dev \
    libproj-dev


ENV PYTHONUNBUFFERED 1

RUN mkdir /fekrino
WORKDIR /fekrino
COPY requirments.txt /fekrino/
RUN pip install -r requirments.txt

COPY . /fekrino/
RUN mkdir /fekrino/logs

# Add any static environment variables needed by Django or your settings file here:
ENV DJANGO_SETTINGS_MODULE=fekrino.settings

RUN python3 manage.py collectstatic --noinput

ENV UWSGI_WSGI_FILE=fekrino/wsgi.py
ENV UWSGI_MASTER=1 UWSGI_WSGI_ENV_BEHAVIOR=holy
ENV UWSGI_WORKERS=2 UWSGI_THREADS=4
ENV UWSGI_SOCKET=fekrino.sock UWSGI_VACUUM=true

USER ${APP_USER}:${APP_USER}

#ENTRYPOINT ["/fekrino/api-entrypoint.sh"]

### Start uWSGI
#CMD ["uwsgi", "--show-config"]

