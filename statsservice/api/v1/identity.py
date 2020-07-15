#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request, current_app
from flask_login import LoginManager, login_user, current_user
from flask_principal import (
    Principal,
    Identity,
    Permission,
    UserNeed,
    RoleNeed,
    session_identity_loader,
    identity_changed,
    identity_loaded
)

from statsservice.bootstrap import application
from statsservice.models import Client


Principal(current_app)
login_manager = LoginManager()
login_manager.init_app(current_app)


client_role = RoleNeed("client")
bo_role = RoleNeed("bo")

client_permission = Permission(client_role)
bo_permission = Permission(bo_role)


@login_manager.user_loader
def load_user(client_id):
    print('load_user')
    return Client.query.filter(Client.id == client_id).first()


@application.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


def login_user_bundle(client):
    print('login_user_bundle')
    login_user(client)
    identity_changed.send(current_app, identity=Identity(client.id))
    print(identity_changed)
    session_identity_loader()


@identity_loaded.connect_via(application)
def on_identity_loaded(sender, identity):
    # Set the identity user object
    print('on_identity_loaded')
    identity.user = current_user

    # Add the UserNeed to the identity
    if current_user.is_authenticated:
        print('auth')
        identity.provides.add(UserNeed(current_user.id))
        identity.provides.add(bo_role)

        # if current_user.role == "client":
        #     identity.provides.add(client_role)
        # if current_user.role == "bo":
        #     identity.provides.add(bo_role)
