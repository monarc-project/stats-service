#! /usr/bin/env bash

if [ ! $# -ge 1 ]
  then
    echo "CLIENT_NAME argument is required, CLIENT_TOKEN is optional. Usage:"
    echo "./create_client.sh CLIENT_NAME CLIENT_TOKEN"
    exit 1
fi

export STATS_CONFIG=production.py

if [ -z "$2" ]
  then
    poetry run flask client_create --name $1
  else
    poetry run flask client_create --name $1 --token $2
fi
