SHELL := /bin/bash

# target: all - Default target. Does nothing.
all:
	@echo "Hello $(LOGNAME), nothing to do by default."
	@echo "Try 'make help'"

help:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

install:
	poetry install

activate:
	poetry shell

run:
	python runserver.py

migrate:
	flask db upgrade

initdb:
	flask db_init

droptestdb:
	dropdb stats-test ; createdb stats-test

inittestdb: droptestdb initdb migrate
	@echo "Done"

superuser:
	flask create_admin --login $(LOGNAME) --password password --email $(LOGNAME)@local.host

update:
	contrib/update.sh

clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

doc:
	rm -Rf docs/_build
	sphinx-multiversion docs/ docs/_build/html