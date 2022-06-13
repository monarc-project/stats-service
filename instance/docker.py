#!/usr/bin/env python3
import os

# Webserver
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 5000))
DEBUG = os.getenv("DEBUG", "0") == "1"
TESTING = os.getenv("TESTING", "0") == "1"
INSTANCE_URL = os.getenv("INSTANCE_URL", f"http://localhost:{PORT}")
FIX_PROXY = os.getenv("FIX_PROXY", "0") == "1"

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "info@cases.lu")
ADMIN_URL = os.getenv("ADMIN_URL", "https://www.cases.lu")

REMOTE_STATS_SERVER = os.getenv("REMOTE_STATS_SERVER", "https://dashboard.monarc.lu")
REMOTE_STATS_TOKEN = os.getenv("REMOTE_STATS_TOKEN", "")
ACTIVE_BLUEPRINTS = ["stats_bp", "admin_bp"]

CLIENT_REGISTRATION_OPEN = os.getenv("CLIENT_REGISTRATION_OPEN", "0") == "1"

DB_HOSTNAME = os.getenv("DB_HOSTNAME", "db")
DB_NAME = os.getenv("DB_NAME", "statsservice")
DB_USERNAME = os.getenv("DB_USERNAME", "statsservice")
DB_PASSWORD = os.getenv("DB_PASSWORD", "statsservice")
DB_PORT = int(os.getenv("DB_PORT", "5432"))

# Database
DB_CONFIG_DICT = {
    "host": DB_HOSTNAME,
    "user": DB_USERNAME,
    "password": DB_PASSWORD,
    "port": DB_PORT,
}

DATABASE_NAME = DB_NAME
SQLALCHEMY_DATABASE_URI = "postgresql://{user}:{password}@{host}:{port}/{name}".format(
    name=DATABASE_NAME, **DB_CONFIG_DICT
)
SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS", "0") == "1"

SECRET_KEY = os.getenv("SECRET_KEY", "LCx3BchmHRxFzkEv4BqQJyeXRLXenf")

LOG_PATH = os.getenv("LOG_PATH", "./var/stats.log")

# Connection with MOSP
MOSP_URL = os.getenv("MOSP_URL", "https://objects.monarc.lu")
