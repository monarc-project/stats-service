#! /usr/bin/env python
from datetime import datetime

from flask import current_app
from flask_login import current_user
from flask_login import login_user
from flask_login import LoginManager
from flask_principal import Identity
from flask_principal import identity_changed
from flask_principal import identity_loaded
from flask_principal import Permission
from flask_principal import Principal
from flask_principal import RoleNeed
from flask_principal import session_identity_loader
from flask_principal import UserNeed

from statsservice.bootstrap import application
from statsservice.bootstrap import db
from statsservice.models import Client
from statsservice.models.client import ROLE_ADMIN
from statsservice.models.client import ROLE_USER


Principal(current_app)
login_manager = LoginManager()
login_manager.init_app(current_app)

user_role = RoleNeed(ROLE_USER)
admin_role = RoleNeed(ROLE_ADMIN)

user_permission = Permission(user_role)
admin_permission = Permission(admin_role)


def login_user_bundle(client):
    if client is None:
        return
    login_user(client)
    identity_changed.send(current_app, identity=Identity(client.id))
    session_identity_loader()


@login_manager.user_loader
def load_user(client_id):
    return Client.query.filter(
        Client.id == client_id, Client.is_active == True  # noqa
    ).first()


@application.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@identity_loaded.connect_via(current_app._get_current_object())  # type: ignore
def on_identity_loaded(sender, identity):
    # Set the identity user object
    identity.user = current_user

    # Add the UserNeed to the identity
    if current_user.is_authenticated:
        identity.provides.add(UserNeed(current_user.id))
        if current_user.role == ROLE_USER:
            identity.provides.add(user_role)
        if current_user.role == ROLE_ADMIN:
            identity.provides.add(admin_role)
