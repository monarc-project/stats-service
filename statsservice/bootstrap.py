#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
from flask import Flask
from flask_mongoengine import MongoEngine
from flask_mongorest import MongoRest


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
    application.config.from_pyfile("production.py", silent=False)

db = MongoEngine(application)
api = MongoRest(application, url_prefix="/api/v2/")
