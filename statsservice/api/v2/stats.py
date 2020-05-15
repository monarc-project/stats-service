from flask import Blueprint
from flask_restx import Api, Resource, fields, reqparse

from statsservice.documents import Stats, Organization


blueprint = Blueprint('api', __name__, url_prefix='/api/v2/stats')
api = Api(blueprint,
    title='MONARC Stats service - API v2',
    version='2.0',
    description='API v2 of the MONARC Stats service',
    doc='/swagger/',
    # All API metadatas
)


# Argument Parsing
parser = reqparse.RequestParser()
parser.add_argument('organization', type=str, help='Organization of the stats')
parser.add_argument('anr', type=str, help='Anr of the stats')
parser.add_argument('type', type=str, help='Type of the stats')
parser.add_argument('day', type=int, help='Type of the stats')
parser.add_argument('month', type=int, help='Type of the stats')
parser.add_argument('year', type=int, help='Type of the stats')
parser.add_argument('page', type=int, default=1, location='args')
parser.add_argument('per_page', type=int, location='args')


# Response marshalling
stats = api.model('Stats', {
    'uuid': fields.String(readonly=True, description='The stats unique identifier'),
    'organization.name': fields.String(readonly=True, description='The stats organization'),
    'anr': fields.String(),
    'type': fields.String(),
    'day': fields.Integer(),
    'week': fields.Integer(),
    'month': fields.Integer(),
    'data': fields.Raw(),
    'created_at': fields.DateTime(),
    'updated_at': fields.DateTime(),
})

stats_list_fields = api.model('StatsList', {
    'metadata': fields.Raw(),
    'data': fields.List(fields.Nested(stats))
})


@api.route('/')
class StatsList(Resource):
    '''Shows a list of all stats, and lets you POST to add new stats'''
    @api.doc('list_stats')
    @api.expect(parser)
    @api.marshal_list_with(stats_list_fields, skip_none=True)
    def get(self):
        '''List all stats'''
        args = parser.parse_args()
        args = {k: v for k, v in args.items() if v is not None}

        page = args.pop("page", 1)
        per_page = args.pop("per_page", 10)

        result = {
            "data": [{}],
            "metadata": {
                "total": 0,
                "count": 0,
                "page": page,
                "per_page": per_page,
            },
        }

        try:
            total = Stats.objects(**args).count()
            stats = Stats.objects(**args).paginate(page=page, per_page=per_page)
            count = len(stats.items)
        except Organization.DoesNotExist:
            return result, 200
        finally:
            if not stats:
                return result, 200

        result["data"] = stats.items
        result["metadata"]["total"] = total
        result["metadata"]["count"] = count

        return result, 200

    @api.doc('create_stats')
    @api.expect(stats)
    @api.marshal_with(stats, code=201)
    def post(self):
        '''Create a new stats'''
        print(api.payload)
        new_stat = Stats(**api.payload)
        return new_stat.save(), 201



@api.route('/<string:uuid>')
@api.response(404, 'Stats not found')
@api.param('uuid', 'The stats identifier')
class StatsItem(Resource):
    '''Show a single stats item and lets you delete them'''
    @api.doc('get_stats')
    @api.marshal_with(stats)
    def get(self, uuid):
        '''Fetch a given resource'''
        return Stats.objects.get(uuid__exact=uuid), 200

    @api.doc('delete_stats')
    @api.response(204, 'Stats deleted')
    def delete(self, uuid):
        '''Delete a stats given its identifier'''
        #DAO.delete(id)
        return '', 204

    @api.expect(stats)
    @api.marshal_with(stats)
    def put(self, uuid):
        '''Update a stats given its identifier'''
        #return DAO.update(id, api.payload)
        pass
