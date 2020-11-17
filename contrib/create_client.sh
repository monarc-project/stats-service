#! /usr/bin/env bash


/home/ansible/.poetry/bin/poetry env use /home/ansible/.pyenv/shims/python

export FLASK_APP=runserver.py
export STATS_CONFIG=production.py

/home/ansible/.poetry/bin/poetry run flask client_create --name $1 --token $2
