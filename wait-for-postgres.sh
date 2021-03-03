#!/bin/sh
# wait-for-postgres.sh

shift

until (! command -v psql || PGPASSWORD=password psql -h db -U "postgres" -c '\q' )
do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"

>&2 echo "Postgres is up - executing command"
RUN poetry run flask db_create
RUN poetry run flask db_init
RUN poetry run flask client_create --name user
RUN poetry run pybabel compile -d statsservice/translations
RUN poetry run flask run
