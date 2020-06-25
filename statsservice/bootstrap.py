#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


ON_HEROKU = int(os.environ.get("HEROKU", 0)) == 1

# Create Flask application
application = Flask(__name__, instance_relative_config=True)

if ON_HEROKU:
    application.config.from_pyfile("heroku.py", silent=False)
    application.config["MONGODB_HOST"] = (
        os.environ.get("MONGODB_URI", "") + "?retryWrites=false"
    )
    application.config["INSTANCE_URL"] = os.environ.get("INSTANCE_URL", "")
else:
    try:
        application.config.from_pyfile("production.py", silent=False)
    except:
        config_file = os.environ.get("FLASK_CONFIG", "")
        application.config.from_pyfile(config_file, silent=False)

db = SQLAlchemy(application)
