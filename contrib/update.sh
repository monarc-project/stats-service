#! /usr/bin/env bash

#
# Update Stats Service.
#

git pull origin master --tags
npm install
poetry install
sudo systemctl restart statsservice.service
