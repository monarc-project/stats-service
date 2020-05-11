from flask_mongorest.views import ResourceView
from flask_mongorest.resources import Resource
from flask_mongorest import operators as ops
from flask_mongorest import methods

from statsapi.bootstrap import api
from statsapi.documents import Stats
from statsapi.api.v1.common import ApiKeyAuthentication


class StatsResource(Resource):
    document = Stats
    filters = {
        "type": [ops.Exact, ops.IExact, ops.Contains, ops.IContains],
        "organization": [ops.Exact],
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


@api.register()
class StatsView(ResourceView):
    resource = StatsResource
    methods = [
        methods.Create,
        methods.Fetch,
        methods.List,
    ]
    authentication_methods = [ApiKeyAuthentication]
