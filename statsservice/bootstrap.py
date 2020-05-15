#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask_mongoengine import MongoEngine
from flask_mongorest import MongoRest


application = Flask(__name__, instance_relative_config=True)
application.config.from_pyfile("production.py", silent=False)

db = MongoEngine(application)
api = MongoRest(application, url_prefix="/api/v1/")
