from flask_mongorest.views import ResourceView
from flask_mongorest.resources import Resource
from flask_mongorest import methods

from statsapi.bootstrap import api
from statsapi.documents.organization import Organization


class OrganizationResource(Resource):
    document = Organization


@api.register()
class OrganizationView(ResourceView):
    resource = OrganizationResource
    methods = [
        methods.Create,
        methods.Update,
        methods.Fetch,
        methods.List,
        methods.Delete,
    ]
