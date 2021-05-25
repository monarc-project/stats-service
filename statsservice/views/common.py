import json
from datetime import datetime
from functools import wraps

from flask import g, current_app, request
from flask.sessions import SecureCookieSessionInterface
from flask_login import login_user, current_user, user_loaded_from_header
from flask_login import LoginManager as OriginalLoginManager
from flask_principal import (
    Principal,
    Identity,
    UserNeed,
    Permission,
    RoleNeed,
    identity_changed,
    identity_loaded,
    session_identity_loader,
)
from statsservice.models.client import ROLE_USER, ROLE_ADMIN
from statsservice.models import Client
from statsservice.bootstrap import application


principals = Principal(current_app)
login_manager = OriginalLoginManager()
login_manager.init_app(current_app)

user_role = RoleNeed(ROLE_USER)
admin_role = RoleNeed(ROLE_ADMIN)

user_permission = Permission(user_role)
admin_permission = Permission(admin_role)


class CustomSessionInterface(SecureCookieSessionInterface):
    """Prevent creating session from API requests."""
    def should_set_cookie(self, *args, **kwargs):
        return False

    def save_session(self, *args, **kwargs):
        if g.get('login_via_header'):
            return
        return super(CustomSessionInterface, self).save_session(*args,
                                                                **kwargs)

application.session_interface = CustomSessionInterface()

@user_loaded_from_header.connect
def user_loaded_from_header(self, user=None):
    g.login_via_header = True


class LoginManager(OriginalLoginManager):
    def init_app(self, app, add_context_processor=True):
        app.session_interface = CustomSessionInterface()
        super().init_app(app, add_context_processor=add_context_processor)


@login_manager.request_loader
def load_user_from_request(request):
    """
    Load user from Authentication header.
    """
    if request.headers.get('X-API-KEY', False):
        user = Client.query.filter(Client.token == request.headers.get('X-API-KEY', False)).first()
        if user:
            print(user)
            login_user(user)
            identity_changed.send(current_app, identity=Identity(user.id))
            return user
        # user_id = current_token.user.id
        # if user_id:
        #     return User.query.get(user_id)
    return None


@login_manager.user_loader
def load_user(client_id):
    return Client.query.filter(Client.id == client_id).first()



@identity_loaded.connect_via(current_app._get_current_object())
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
