#! /usr/bin/env bash

#
# Update Stats Service.
#

git pull origin master --tags
npm install
poetry install
poetry run flask db upgrade
sudo systemctl restart statsservice.service
