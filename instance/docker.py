# Webserver
HOST = "0.0.0.0"
PORT = 5000
DEBUG = True
TESTING = False
INSTANCE_URL = "http://127.0.0.1:5000"

ADMIN_EMAIL = "info@cases.lu"
ADMIN_URL = "https://www.cases.lu"

REMOTE_STATS_SERVER = 'https://dashboard.monarc.lu'
REMOTE_STATS_TOKEN = ""

# Database
DB_CONFIG_DICT = {
    "user": "postgres",
    "password": "password",
    "host": "db",
    "port": 5432,
}
DATABASE_NAME = "statsservice"
SQLALCHEMY_DATABASE_URI = "postgresql://{user}:{password}@{host}:{port}/{name}".format(
    name=DATABASE_NAME, **DB_CONFIG_DICT
)
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = 'LCx3BchmHRxFzkEv4BqQJyeXRLXenf'

LOG_PATH = "./var/stats.log"

# Connection with MOSP
MOSP_URL = "https://objects.monarc.lu"
