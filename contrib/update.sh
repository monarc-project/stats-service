#! /usr/bin/env bash

#
# Update Stats Service.
#

git pull origin master --tags
npm install
poetry install --no-dev
poetry run pybabel compile -d statsservice/translations
poetry run flask db upgrade
sudo systemctl restart statsservice.service
