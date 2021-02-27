FROM ubuntu:focal
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get -y install wget python3-dev git python3-venv python3-pip
RUN pip3 install poetry

WORKDIR statsservice

COPY statsservice statsservice/
COPY contrib contrib/
COPY instance instance/
COPY pyproject.toml .
COPY poetry.lock .
COPY package.json .
COPY package-lock.json .
COPY README.md .

RUN poetry install

ENV FLASK_APP runserver.py
ENV FLASK_ENV development

RUN FLASK_APP=runserver.py poetry run flask db_create
RUN FLASK_APP=runserver.py poetry run flask db_init
RUN FLASK_APP=runserver.py poetry run flask client_create --name user
