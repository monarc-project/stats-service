FROM ubuntu:focal
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get -y install python-dev python3-setuptools python-virtualenv git npm wget
RUN pip3 install poetry

WORKDIR statsservice

COPY statsservice statsservice/
COPY contrib contrib/
COPY instance instance/
COPY migrations migrations/
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

RUN poetry install --no-dev

ENV FLASK_APP runserver.py
ENV FLASK_ENV development
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000
ENV STATS_CONFIG docker.py

EXPOSE 5000
CMD ["./wait-for-postgres.sh", "db"]
