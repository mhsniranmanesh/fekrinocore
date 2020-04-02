# FROM python:3
# docker build -t ubuntu1604py36
FROM ubuntu:16.04

RUN apt-get update
RUN apt-get install -y software-properties-common vim
RUN add-apt-repository ppa:jonathonf/python-3.6
RUN apt-get update

RUN apt-get install -y build-essential python3.6 python3.6-dev python3-pip python3.6-venv
RUN apt-get install -y git

RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.5 1
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 2

# update pip
RUN python3.6 -m pip install pip --upgrade
RUN python3.6 -m pip install wheel

RUN apt-get install -y gdal-bin \
    libgdal-dev \
    python3-gdal \
    binutils \
    libpq-dev \
    libproj-dev


ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code
COPY ./piprequirments.txt /code/
RUN pip install -r piprequirments.txt

COPY . /code/
# CMD [ "./run.sh"]
# CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]