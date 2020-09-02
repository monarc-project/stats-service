#! /usr/bin/env python
# -*- coding: utf-8 -*-


class Config(object):
    HOST = "127.0.0.1"
    PORT = 5000
    INSTANCE_URL = "http://127.0.0.1:5000"
    DEBUG = False
    TESTING = False

    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

    ADMIN_EMAIL = "info@cases.lu"
    ADMIN_URL = "https://www.cases.lu"

    REMOTE_STATS_SERVER = "http://127.0.0.1:5000"

    SECRET_KEY = "LCx3BchmHRxFzkEv4BqQJyeXRLXenf"

    LOG_PATH = "./var/stats.log"

    # Connection with MOSP
    MOSP_URL = "https://objects.monarc.lu"


class ProductionConfig(Config):
    DB_CONFIG_DICT = {
        "user": "pgsqluser",
        "password": "pgsqlpwd",
        "host": "localhost",
        "port": 5432,
    }
    DATABASE_NAME = "statsservice"
    SQLALCHEMY_DATABASE_URI = "postgresql://{user}:{password}@{host}:{port}/{name}".format(
        name=DATABASE_NAME, **DB_CONFIG_DICT
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
