#! /usr/bin/env python
import io
import logging
import os
import re
import uuid
from typing import Any

from flask import Flask
from flask import request
from flask_babel import Babel
from flask_babel import format_datetime
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.routing import BaseConverter
from werkzeug.routing import ValidationError


def set_logging(
    log_path=None,
    log_level=logging.INFO,
    modules=(),
    log_format="%(asctime)s %(levelname)s %(name)s %(funcName)s %(lineno)s: %(message)s",
):
    if not modules:
        modules = (
            "root",
            "runserver",
            "statsservice.api.v1.client",
            "statsservice.api.v1.stats",
            "statsservice.api.v1.processed",
            "statsservice.commands.stats",
        )
    handler = io.BytesIO()  # type: Any
    if log_path:
        if not os.path.exists(os.path.dirname(log_path)):
            os.makedirs(os.path.dirname(log_path))
        if not os.path.exists(log_path):
            open(log_path, "w").close()
        handler = logging.FileHandler(log_path)
    else:
        handler = logging.StreamHandler()
    formater = logging.Formatter(log_format)
    handler.setFormatter(formater)
    for logger_name in modules:
        logger = logging.getLogger(logger_name)
        logger.addHandler(handler)
        for handler in logger.handlers:
            handler.setLevel(log_level)
        logger.setLevel(log_level)


# Create Flask application
application = Flask(__name__, instance_relative_config=True)

# Load the appropriate configuration
TESTING = os.environ.get("testing", "") == "actions"
if TESTING:
    # Testing on GitHub Actions
    application.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = "postgresql://statsservice:password@localhost:5432/statsservice"
elif os.environ.get("STATS_CONFIG", ""):
    # if a specific configuration is provided by the user
    # this does not works with mod_wsgi
    config_file = os.environ.get("STATS_CONFIG", "")
    application.config.from_pyfile(config_file, silent=False)
else:
    try:
        application.config.from_pyfile("production.py", silent=False)
    except Exception:
        # default configuration file
        application.config.from_object("instance.config.ProductionConfig")

if not application.config.get("ACTIVE_BLUEPRINTS", False):
    application.config["ACTIVE_BLUEPRINTS"] = ["stats_bp", "admin_bp"]

# Set SECRET_KEY if it was not defined
if not application.config.get("SECRET_KEY", False):
    application.config["SECRET_KEY"] = os.urandom(24)

if application.config.get("FIX_PROXY", False):
    application.wsgi_app = ProxyFix(application.wsgi_app, x_host=1, x_prefix=1)  # type: ignore

set_logging(application.config.get("LOG_PATH", None))


db = SQLAlchemy(application)
migrate = Migrate(application, db)


# Internationalization
babel = Babel(application)


@babel.localeselector
def get_locale():
    # if a user is logged in, use the locale from the user settings
    # user = getattr(g, 'user', None)
    # if user is not None:
    #     return user.locale
    # otherwise try to guess the language from the user accept
    # header the browser transmits.  We support de/fr/en in this
    # example.  The best match wins.
    return request.accept_languages.best_match(["fr", "en"])


application.jinja_env.filters["datetime"] = format_datetime

application.jinja_env.trim_blocks = True
application.jinja_env.lstrip_blocks = True

# URL Converters: UUID type
UUID_RE = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")


class UUIDConverter(BaseConverter):
    """
    UUID converter for the Werkzeug routing system.
    """

    def __init__(self, map, strict=True):
        super().__init__(map)
        self.strict = strict

    def to_python(self, value):
        if self.strict and not UUID_RE.match(value):
            raise ValidationError()
        try:
            return uuid.UUID(value)
        except ValueError:
            raise ValidationError()

    def to_url(self, value):
        return str(value)


application.url_map.converters["uuid"] = UUIDConverter
