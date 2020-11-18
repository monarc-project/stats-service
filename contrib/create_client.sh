#! /usr/bin/env bash

if [ ! $# -eq 2 ]
  then
    echo "Two arguments are required. Usage:"
    echo "./create_client.sh CLIENT_NAME CLIENT_TOKEN"
    exit 1
fi

#export FLASK_APP=runserver.py
#export STATS_CONFIG=production.py

#poetry env use /home/ansible/.pyenv/shims/python


poetry run flask client_create --name $1 --token $2
