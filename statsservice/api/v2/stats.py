from flask import Blueprint
from flask_restx import Api, Resource, fields, reqparse

from statsservice.documents import Stats, Organization


blueprint = Blueprint("api", __name__, url_prefix="/api/v2/stats")
api = Api(
    blueprint,
    title="MONARC Stats service - API v2",
    version="2.0",
    description="API v2 of the MONARC Stats service.",
    doc="/swagger/",
    # All API metadatas
)


# Argument Parsing
parser = reqparse.RequestParser()
parser.add_argument("organization", type=str, help="Organization of the stats")
parser.add_argument("anr", type=str, help="UUID of the Anr of the stats")
parser.add_argument(
    "type", type=str, help="Type of the stats (risk, vulnerability, threat)"
)
parser.add_argument("day", type=int, help="Day of the stats")
parser.add_argument("week", type=int, help="Week of the stats")
parser.add_argument("month", type=int, help="Month of the stats")
parser.add_argument("year", type=int, help="Year of the stats")
parser.add_argument("page", type=int, default=1, location="args")
parser.add_argument("per_page", type=int, location="args")


# Response marshalling
stats = api.model(
    "Stats",
    {
        "uuid": fields.String(readonly=True, description="The stats unique identifier"),
        "organization": fields.String(
            readonly=True,
            attribute=lambda x: x.organization.name,
            description="The organization related to this stats.",
        ),
        "anr": fields.String(description="The ANR related to this stats."),
        "type": fields.String(
            description="The type of this stats (risk, vulnerability, threat)."
        ),
        "day": fields.Integer(description="Day of the stats."),
        "week": fields.Integer(description="Week of the stats."),
        "month": fields.Integer(description="Month of the stats."),
        "year": fields.Integer(description="Year of the stats."),
        "data": fields.Raw(description="The stats as a dynamic JSON object."),
        "created_at": fields.DateTime(description="Created time of the stats."),
        "updated_at": fields.DateTime(description="Updated time of the stats."),
    },
)

stats_list_fields = api.model(
    "StatsList",
    {
        "metadata": fields.Raw(
            description="Metada related to the result (number of page, current page, total number of objects.)."
        ),
        "data": fields.List(fields.Nested(stats), description="List of stats objects"),
    },
)


@api.route("/")
class StatsList(Resource):
    """Shows a list of all stats, and lets you POST to add new stats"""

    @api.doc("list_stats")
    @api.expect(parser)
    @api.marshal_list_with(stats_list_fields, skip_none=True)
    def get(self):
        """List all stats"""
        args = parser.parse_args()
        args = {k: v for k, v in args.items() if v is not None}

        page = args.pop("page", 1)
        per_page = args.pop("per_page", 10)

        result = {
            "data": [],
            "metadata": {"total": 0, "count": 0, "page": page, "per_page": per_page,},
        }

        try:
            total = Stats.objects(**args).count()
            stats = Stats.objects(**args).paginate(page=page, per_page=per_page)
            count = len(stats.items)
        except Organization.DoesNotExist:
            return result, 200
        except Exception as e:
            print(e)
        finally:
            if not total:
                print(result)
                return result, 200

        result["data"] = stats.items
        result["metadata"]["total"] = total
        result["metadata"]["count"] = count

        return result, 200

    @api.doc("create_stats")
    @api.expect(stats)
    @api.marshal_with(stats, code=201)
    def post(self):
        """Create a new stats"""
        new_stat = Stats(**api.payload)
        return new_stat.save(), 201


@api.route("/<string:uuid>")
@api.response(404, "Stats not found")
@api.param("uuid", "The stats identifier")
class StatsItem(Resource):
    """Show a single stats item and lets you delete them"""

    @api.doc("get_stats")
    @api.marshal_with(stats)
    def get(self, uuid):
        """Fetch a given resource"""
        return Stats.objects.get(uuid__exact=uuid), 200

    @api.doc("delete_stats")
    @api.response(204, "Stats deleted")
    def delete(self, uuid):
        """Delete a stats given its identifier"""
        # DAO.delete(id)
        return "", 204

    @api.expect(stats)
    @api.marshal_with(stats)
    def put(self, uuid):
        """Update a stats given its identifier"""
        # return DAO.update(id, api.payload)
        pass
