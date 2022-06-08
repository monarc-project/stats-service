#! /usr/bin/env python
# Stats service API for MONARC
# Copyright (C) 2020-2022 Cédric Bonhomme - https://www.cedricbonhomme.org
# Copyright (C) 2020-2022 SMILE gie securitymadein.lu
#
# For more information: https://github.com/monarc-project/stats-api/
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from statsservice.bootstrap import application
from statsservice.commands import client_coordinates_set
from statsservice.commands import client_coordinates_unset
from statsservice.commands import client_create
from statsservice.commands import client_delete
from statsservice.commands import client_list
from statsservice.commands import client_sharing_activate
from statsservice.commands import client_sharing_deactivate
from statsservice.commands import db_create
from statsservice.commands import db_empty
from statsservice.commands import db_init
from statsservice.commands import mosp_is_object_published
from statsservice.commands import stats_delete
from statsservice.commands import stats_pull
from statsservice.commands import stats_push


def register_commands(app):
    """Register Click commands."""
    # database
    app.cli.add_command(db_empty)
    app.cli.add_command(db_create)
    app.cli.add_command(db_init)
    # client
    app.cli.add_command(client_create)
    app.cli.add_command(client_list)
    app.cli.add_command(client_delete)
    app.cli.add_command(client_coordinates_set)
    app.cli.add_command(client_coordinates_unset)
    app.cli.add_command(client_sharing_activate)
    app.cli.add_command(client_sharing_deactivate)
    # stats
    app.cli.add_command(stats_delete)
    app.cli.add_command(stats_push)
    app.cli.add_command(stats_pull)
    # mosp
    app.cli.add_command(mosp_is_object_published)


with application.app_context():
    from statsservice.api import v1

    application.register_blueprint(v1.api_blueprint)

    from statsservice import views

    for blueprint in views.__all__:
        if blueprint in application.config["ACTIVE_BLUEPRINTS"]:
            application.register_blueprint(getattr(views, blueprint))

    register_commands(application)


def run():
    application.run(
        host=application.config["HOST"],
        port=application.config["PORT"],
        debug=application.config["DEBUG"],
    )


if __name__ == "__main__":
    run()
