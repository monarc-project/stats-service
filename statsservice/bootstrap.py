#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# Create Flask application
application = Flask(__name__, instance_relative_config=True)

# Load the appropriate configuration
ON_HEROKU = int(os.environ.get("HEROKU", 0)) == 1
TESTING = os.environ.get("testing", "") == "actions"
if TESTING:
    # Testing on GitHub Actions
    application.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = "postgresql://statsservice:password@localhost:5432/statsservice"
elif ON_HEROKU:
    # if the application is running on Heroku
    application.config.from_pyfile("heroku.py", silent=False)
    application.config["INSTANCE_URL"] = os.environ.get("INSTANCE_URL", "")
elif os.environ.get("STATS_CONFIG", ""):
    # if a specific configuration is provided by the user
    config_file = os.environ.get("STATS_CONFIG", "")
    application.config.from_pyfile(config_file, silent=False)
else:
    # default configuration file
    application.config.from_object("instance.config.ProductionConfig")

# Set SECRET_KEY if it was not defined
if not application.config.get("SECRET_KEY", False):
    application.config["SECRET_KEY"] = os.urandom(24)

db = SQLAlchemy(application)
