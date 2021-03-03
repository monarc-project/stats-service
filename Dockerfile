FROM python:3.9-alpine
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive

RUN apk update && \
  apk add \
  build-base \
  curl \
  git \
  python3-dev \
  gettext \
  freetype-dev \
  libffi-dev \
  openssl-dev \
  libxml2-dev \
  libxslt-dev \
  libpq \
  postgresql-client \
  postgresql-dev \
  libressl-dev \
  musl-dev \
  npm

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

RUN pip install poetry
RUN poetry install

ENV FLASK_APP runserver.py
ENV FLASK_ENV development
