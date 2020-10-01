from flask import Blueprint, request, render_template
from flask_restx import Api

from statsservice.bootstrap import application


api_blueprint = Blueprint("api", __name__, url_prefix="/api/v1")


def setup_api(application):
    authorizations = {
        "apikey": {
            "type": "apiKey",
            "in": "header",
            "name": "X-API-KEY",
        }
    }

    api = Api(
        api_blueprint,
        title="MONARC Stats service - API v1",
        version="1.0",
        description="API v1 of the MONARC Stats service.",
        license="GNU Affero General Public License version 3",
        license_url="https://www.gnu.org/licenses/agpl-3.0.html",
        doc="/",
        security="apikey",
        authorizations=authorizations,
        contact_email=application.config["ADMIN_EMAIL"],
        contact_url=application.config["ADMIN_URL"],
    )

    @api.documentation
    def custom_ui():
        return render_template(
            "swagger-ui.html",
            title=api.title,
            specs_url="{}/api/v1/swagger.json".format(
                application.config["INSTANCE_URL"]
            ),
        )

    from statsservice.api.v1 import stats, client, processed

    api.add_namespace(client.client_ns, path="/client")
    api.add_namespace(stats.stats_ns, path="/stats")
    api.add_namespace(processed.processed_ns, path="/stats/processed")

    return api


api = setup_api(application)
