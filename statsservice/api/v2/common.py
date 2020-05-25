from flask import request
from flask_mongorest.authentication import AuthenticationBase

from statsservice.bootstrap import application
from statsservice.documents import Organization


class ApiKeyAuthentication(AuthenticationBase):
    """Custom token based authentication.
    """

    def authorized(self):
        if "X-API-KEY" in request.headers:
            token = request.headers.get("X-API-KEY", False)
            if token:
                try:
                    organization = Organization.objects.get(token__exact=token)
                    return True
                except (TypeError, UnicodeDecodeError, Organization.DoesNotExist):
                    pass
        return False
