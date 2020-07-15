#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request, current_app
from flask_login import login_user, current_user
from flask_principal import (
    Identity,
    Permission,
    RoleNeed,
    session_identity_loader,
    identity_changed,
    identity_loaded
)


client_role = RoleNeed("client")
bo_role = RoleNeed("bo")

client_permission = Permission(client_role)
bo_permission = Permission(bo_role)


def login_user_bundle(user):
    login_user(user)
    identity_changed.send(current_app, identity=Identity(user.id))
    session_identity_loader()


@identity_loaded.connect_via(current_app._get_current_object())
def on_identity_loaded(sender, identity):
    # Set the identity user object
    identity.user = current_user

    # Add the UserNeed to the identity
    if current_user.is_authenticated:
        identity.provides.add(UserNeed(current_user.id))
        if current_user.role == "client":
            identity.provides.add(client_role)
        if current_user.role == "bo":
            identity.provides.add(bo_role)
