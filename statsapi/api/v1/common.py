from flask import request
from flask_mongorest.authentication import AuthenticationBase

from statsapi.bootstrap import application
from statsapi.documents import Organization


class ApiKeyAuthentication(AuthenticationBase):
    """Custom token based authentication. To be inproved."""

    def authorized(self):
        if not application.config["API_KEY_AUTHENTICATION"]:
            return True
        if "AUTHORIZATION" in request.headers:
            authorization = request.headers["AUTHORIZATION"].split()
            if len(authorization) == 2 and authorization[0].lower() == "basic":
                try:
                    token = authorization[1]
                    token_key = Organization.objects.get(token__exact=token)
                    print(token_key)
                    # if token_key.user:
                    #     login_user(token_key.user)
                    #     setattr(current_user, 'token_key', token_key)
                    return True
                except (TypeError, UnicodeDecodeError, Organization.DoesNotExist):
                    pass
        return False
