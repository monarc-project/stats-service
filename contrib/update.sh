#! /usr/bin/env bash

#
# Update Stats Service.
#

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

set -e
#set -x

git pull origin master --tags
npm ci
poetry install --only main
poetry run pybabel compile -d statsservice/translations
poetry run flask db upgrade

echo -e "✨ 🌟 ✨"
echo -e "${GREEN}Stats Service updated. You can now restart the service.${NC} Examples:"
echo "    sudo systemctl restart statsservice.service"
echo "    sudo systemctl restart apache2.service"

exit 0
