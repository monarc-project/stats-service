from flask import current_app
from flask import g
from flask.sessions import SecureCookieSessionInterface
from flask_login import current_user
from flask_login import login_user
from flask_login import LoginManager as OriginalLoginManager
from flask_login import user_loaded_from_header
from flask_principal import Identity
from flask_principal import identity_changed
from flask_principal import identity_loaded
from flask_principal import Permission
from flask_principal import Principal
from flask_principal import RoleNeed
from flask_principal import UserNeed

from statsservice.bootstrap import application
from statsservice.models import Client
from statsservice.models.client import ROLE_ADMIN
from statsservice.models.client import ROLE_USER


principals = Principal(current_app)
login_manager = OriginalLoginManager()
login_manager.init_app(current_app)


# Definitions of roles and permissions
user_role = RoleNeed(ROLE_USER)
admin_role = RoleNeed(ROLE_ADMIN)

user_permission = Permission(user_role)
admin_permission = Permission(admin_role)


class CustomSessionInterface(SecureCookieSessionInterface):
    """Prevent creating session from API requests (/admin endpoints)."""

    def should_set_cookie(self, *args, **kwargs):
        return False

    def save_session(self, *args, **kwargs):
        if g.get("login_via_header"):
            return
        return super().save_session(*args, **kwargs)


application.session_interface = CustomSessionInterface()


@user_loaded_from_header.connect
def user_loaded_from_header_custom(self, user=None):
    g.login_via_header = True


class LoginManager(OriginalLoginManager):
    def init_app(self, app, add_context_processor=True):
        app.session_interface = CustomSessionInterface()
        super().init_app(app, add_context_processor=add_context_processor)


@login_manager.request_loader
def load_user_from_request(request):
    """Load user from authentication header."""
    token = request.headers.get("X-API-KEY", False)
    if token:
        user = Client.query.filter(Client.token == token).first()
        if user:
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
