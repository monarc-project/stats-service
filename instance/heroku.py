import os

HOST = "0.0.0.0"
PORT = os.environ.get("PORT")
DEBUG = False
TESTING = False
INSTANCE_URL = ""

ADMIN_EMAIL = "info@cases.lu"
ADMIN_URL = "https://www.cases.lu"

SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
SQLALCHEMY_TRACK_MODIFICATIONS = False

REMOTE_STATS_SERVER = "http://127.0.0.1:5000"

SECRET_KEY = "LCx3BchmHRxFzkEv4BqQJyeXRLXenf"

LOG_PATH = ""

# Connection with MOSP
MOSP_URL = "https://objects.monarc.lu"
