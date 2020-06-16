#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Stats service API for MONARC
# Copyright (C) 2020 Cédric Bonhomme - https://www.cedricbonhomme.org
# Copyright (C) 2020 SMILE gie securitymadein.lu
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

from flask import Blueprint

from statsservice.models import Stats

stats_bp = Blueprint("stats_bp", __name__, url_prefix="/stats")


@stats_bp.route("/risks.json", methods=["GET"])
def risks():
    """
    """
    risks = Stats.query.filter(Stats.type == "risk").all()
    # risks = Stats.objects(**{'{}__{}'.format(field, operator): 18})
    # risks = Stats.objects(data__anr__exact=2)
    return risks.to_json()
