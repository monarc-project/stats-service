#!/bin/sh
# wait-for-postgres.sh

shift

until (! command -v psql || PGPASSWORD=password psql -h db -U "postgres" -c '\q' )
do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"
poetry run flask db_create
poetry run flask db_init
poetry run flask client_create --name user
poetry run pybabel compile -d statsservice/translations
poetry run flask run
