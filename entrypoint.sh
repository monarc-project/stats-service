#!/bin/sh

if [ "$DEBUG" ]; then
	set -x
fi
set -eu

FLASK_ENV="$ENVIRONMENT"
FLASK_DEBUG="$DEBUG"
FLASK_RUN_HOST="$HOST"
FLASK_RUN_PORT="$PORT"

export FLASK_ENV FLASK_DEBUG FLASK_RUN_HOST FLASK_RUN_PORT

prepare_db() {
	flask db_create || true
	flask db_init
	flask db upgrade
	if [ "$ADMIN_TOKEN" ]; then
		flask client_create --name admin --role admin --token "$ADMIN_TOKEN" || true
	fi
}

# waiting for DB to come up
for try in 1 2 3 4 5 6; do
	echo >&2 "migration - attempt $try"
	prepare_db && break || true
	sleep 5
	[ "$try" = "6" ] && exit 1
done

flask run
