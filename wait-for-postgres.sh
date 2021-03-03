#!/bin/sh
# wait-for-postgres.sh

set -e

host="$1"
shift
cmd="$@"

until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$host" -U "postgres" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"
RUN poetry run flask db_create
RUN poetry run flask db_init
RUN poetry run flask client_create --name user
RUN poetry run pybabel compile -d statsservice/translations
RUN poetry run flask run
