from flask import request
from flask_mongorest.views import ResourceView
from flask_mongorest.resources import Resource
from flask_mongorest import operators as ops
from flask_mongorest import methods

from statsapi.bootstrap import api
from statsapi.documents import Stats, Organization
from statsapi.api.v1.common import ApiKeyAuthentication


class StatsResource(Resource):
    document = Stats
    filters = {
        "type": [ops.Exact, ops.IExact, ops.Contains, ops.IContains],
        "organization": [ops.Exact],
        "day": [ops.Exact],
        "month": [ops.Exact],
        "year": [ops.Exact],
        "created_at": [ops.Exact, ops.IExact, ops.Contains, ops.IContains],
    }
    # fields = ['type', 'uuid']
    # filters = {"created_at": [ops.Exact]}
    paginate = True
    default_limit = 100
    max_limit = 1000
    bulk_update_limit = 100

    def uuid(self, obj):
        return str(obj.uuid)

    def save_object(self, obj, **kwargs):
        """Overrides save_object in order to set obj.organization with the
        organization associated to the submitted token.
        """
        # TODO: improve the way we retrieve this token
        token = request.headers.get("X-API-KEY", False)
        organization = Organization.objects.get(token__exact=token)
        obj.organization = organization
        return super(StatsResource, self).save_object(obj, **kwargs)

    # def get_objects(self, **kwargs):
    #     qs, has_more = super(StatsResource, self).get_objects(**kwargs)
    #     print(qs)
    #     return qs, has_more, {'more': 'stuff'}
    #
    # def update_object(self, obj, data=None, save=True, parent_resources=None):
    #     data = data or self.data
    #     print(data)
    #     if data.get('author'):
    #         author = data['author']
    #         if author.email == 'vincent@vangogh.com':
    #             obj.tags.append('art')
    #     return super(StatsResource, self).update_object(obj, data, save, parent_resources)


@api.register()
class StatsView(ResourceView):
    resource = StatsResource
    methods = [
        methods.Create,
        methods.Fetch,
        methods.List,
    ]
    authentication_methods = [ApiKeyAuthentication]

    # def post(self, **kwargs):
    #     return super(StatsView, self).post(**kwargs)
