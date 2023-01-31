import sqlalchemy
from flask import Blueprint
from flask import render_template
from flask_restx import Api

from statsservice.bootstrap import application
from statsservice.bootstrap import db


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
        description="<a href='https://www.nc3.lu' target='_blank' rel='noopener noreferrer'>NC3 Luxembourg</a><br />"  # noqa
        + "API v1 of the MONARC Stats service.<br />"
        + "This is the API used by the <a href='https://www.monarc.lu' target='_blank' rel='noopener noreferrer'>MONARC software</a> for its global dashboard.<br /><br />"  # noqa
        + "Source code: https://github.com/monarc-project/stats-service<br />"
        + "A <a href='https://www.monarc.lu/documentation/stats-service/api-v1.html' target='_blank' rel='noopener noreferrer'>documentation is availabe</a> with some examples.<br /><br />"  # noqa
        + "Responsible of this instance: "
        + application.config["ADMIN_EMAIL"],
        license="GNU Affero General Public License version 3",
        license_url="https://www.gnu.org/licenses/agpl-3.0.html",
        doc="/",
        security="apikey",
        authorizations=authorizations,
        contact_email=application.config["ADMIN_EMAIL"],
        contact_url=application.config["ADMIN_URL"],
    )

    @api.errorhandler(sqlalchemy.exc.IntegrityError)
    def handle_duplicate_object_exception(error):
        """Return a 304 status code on SQLALchemy IntegrityError."""
        db.session.rollback()
        return {"message": "Duplicate object."}, 304

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
