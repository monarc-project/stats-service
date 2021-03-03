FROM ubuntu:focal
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get -y install wget python3-dev git python3-venv python3-pip npm
RUN pip3 install poetry

WORKDIR statsservice

COPY statsservice statsservice/
COPY contrib contrib/
COPY instance instance/
COPY runserver.py .
COPY pyproject.toml .
COPY poetry.lock .
COPY package.json .
COPY package-lock.json .
COPY README.md .
COPY wait-for-postgres.sh .

RUN chmod +x ./wait-for-postgres.sh

RUN mkdir node_modules
RUN npm install
RUN mkdir -p statsservice/static/npm_components
RUN cp -R node_modules/* statsservice/static/npm_components/

RUN poetry install

ENV FLASK_APP runserver.py
ENV FLASK_ENV development
