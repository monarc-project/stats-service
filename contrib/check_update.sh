#! /usr/bin/env bash

#
# Check if a release is available.
#

version='0.4'
timestamp=`date +%s`

useragent="Stats-Service/$version (`uname -s`; `uname -o`; `uname -p`) `lsb_release -ds | tr ' ' '-'`"

curl --request GET  \
-A "$useragent" \
-H "Content-type: application/json" \
-H "Accept: application/json" \
-d '{"version": "'$version'", "timestamp": "'$timestamp'"}' \
'https://version.monarc.lu/check/Stats-Service' >> image.svg

xdg-open image.svg

rm image.svg
