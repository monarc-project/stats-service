#! /usr/bin/env bash

#
# Install the Stats service with its dependencies and enable a new systemd service.
#


RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

ME=`whoami`

STATS_PATH="/home/$ME/stats-service"
STATS_HOST='0.0.0.0'
STATS_PORT='5005'
STATS_DB_NAME='statsservice'
STATS_DB_USER='dbstatsuser'
STATS_DB_PASSWORD='dbstatsuser'
STATS_SECRET_KEY="$(openssl rand -hex 32)"


# Installation of dependencies
sudo apt-get -y install postgresql python3-pip python3-venv
sudo update-alternatives --install /usr/bin/python python /usr/bin/python2 10
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3 20
sudo -u postgres psql -c "CREATE USER $STATS_DB_USER WITH PASSWORD '$STATS_DB_PASSWORD';"
sudo -u postgres psql -c "ALTER USER $STATS_DB_USER WITH SUPERUSER;"


# Installation of Poetry
cd ~
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
echo  'export PATH="$PATH:$HOME/.poetry/bin"' >> ~/.bashrc
source ~/.bashrc
source $HOME/.poetry/env


# Retrieve source code of stats-service
git clone https://github.com/monarc-project/stats-service $STATS_PATH
cd $STATS_PATH
poetry install --no-dev

echo  'export FLASK_APP=runserver.py' >> ~/.bashrc
echo  'export STATS_CONFIG=production.py' >> ~/.bashrc
source ~/.bashrc

# Create the configuration file
bash -c "cat << EOF > $STATS_PATH/instance/production.py
HOST = '$STATS_HOST'
PORT = $STATS_PORT
DEBUG = False
TESTING = False
INSTANCE_URL = 'http://127.0.0.1:$STATS_PORT'

ADMIN_EMAIL = 'info@cases.lu'
ADMIN_URL = 'https://www.cases.lu'

REMOTE_STATS_SERVER = 'https://dashboard.monarc.lu'

DB_CONFIG_DICT = {
    'user': '$STATS_DB_USER',
    'password': '$STATS_DB_PASSWORD',
    'host': 'localhost',
    'port': 5432,
}
DATABASE_NAME = '$STATS_DB_NAME'
SQLALCHEMY_DATABASE_URI = 'postgres://{user}:{password}@{host}:{port}/{name}'.format(
    name=DATABASE_NAME, **DB_CONFIG_DICT
)
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = '$STATS_SECRET_KEY'

MOSP_URL = 'https://objects.monarc.lu'
EOF"


# Initializes the database
export FLASK_APP=runserver.py
export STATS_CONFIG=production.py

FLASK_APP=runserver.py poetry run flask db_create
FLASK_APP=runserver.py poetry run flask db_init
FLASK_APP=runserver.py poetry run flask client_create --name ADMIN --role admin


# Create a systemd service
sudo bash -c "cat << EOF > /etc/systemd/system/statsservice.service
[Unit]
Description=MONARC Stats service
After=network.target

[Service]
User=$ME
Environment=LANG=en_US.UTF-8
Environment=LC_ALL=en_US.UTF-8
Environment=FLASK_APP=runserver.py
Environment=FLASK_ENV=production
Environment=STATS_CONFIG=production.py
Environment=FLASK_RUN_HOST=$STATS_HOST
Environment=FLASK_RUN_PORT=$STATS_PORT
WorkingDirectory=$STATS_PATH
ExecStart=/home/$ME/.poetry/bin/poetry run flask run
Restart=always

[Install]
WantedBy=multi-user.target
EOF"

sudo systemctl daemon-reload > /dev/null
sleep 1
sudo systemctl enable statsservice.service > /dev/null
sleep 3
sudo systemctl restart statsservice > /dev/null



echo -e "Stats service is ready and available at http://127.0.0.1:$STATS_PORT"
