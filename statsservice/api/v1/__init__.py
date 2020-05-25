from flask import request, Blueprint
from flask_restx import Api

from statsservice.bootstrap import application


api_blueprint = Blueprint("api", __name__, url_prefix="/api/v1")


def setup_api(application):
    authorizations = {
        'apikey': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'X-API-KEY',
        }
    }

    api = Api(
        api_blueprint,
        title="MONARC Stats service - API v2",
        version="2.0",
        description="API v1 of the MONARC Stats service.",
        license="GNU Affero General Public License version 3",
        license_url="https://www.gnu.org/licenses/agpl-3.0.html",
        doc="/",
        security='apikey',
        authorizations=authorizations,
        contact_email=application.config["ADMIN_EMAIL"],
        contact_url=application.config["ADMIN_URL"]
    )

    from statsservice.api.v2 import stats

    api.add_namespace(stats.stats_ns, path="/api/v1/stats")

    return api


api = setup_api(application)
