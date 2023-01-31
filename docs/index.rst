.. MONARC Stats Service documentation master file, created by
   sphinx-quickstart on Tue Apr 28 15:01:17 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


Presentation
============

`MONARC Stats Service <https://github.com/monarc-project/stats-service>`_ is a libre
software which is providing:

* an API in order to **collect** statistics from one or several
  `MONARC <https://github.com/monarc-project/MonarcAppFO>`_ instances and to **return**
  these statistics with different filters and aggregation methods;
* a dashboard that summarizes the **current cybersecurity landscape**. The charts are
  based on the collected statistics.

This software can be deployed just next to a MONARC instance or on a
dedicated server.

The collected statistics can be sent to an other Stats Service instance.

.. note::

    The public official instance operated by `NC3 <https://www.nc3.lu>`_ is
    available at `dashboard.monarc.lu <https://dashboard.monarc.lu>`_.



.. toctree::
   :caption: Technical considerations
   :maxdepth: 3
   :hidden:

   installation
   updates
   command-line-interface
   logging
   modules


.. toctree::
   :caption: Conceptual considerations
   :maxdepth: 3
   :hidden:

   architecture


.. toctree::
   :caption: Blueprints
   :maxdepth: 3
   :hidden:

   blueprints


Bugs
====

Please report bugs to:

https://github.com/monarc-project/stats-service/issues



License
=======

MONARC Stats Service is licensed under
`GNU Affero General Public License version 3 <https://www.gnu.org/licenses/agpl-3.0.html>`_.


MONARC Stats Service.

* Copyright (C) 2020-2022 Cédric Bonhomme
* Copyright (C) 2020-2022 Juan Rocha
* Copyright (C) 2020-2021 NC3

For more information: https://github.com/monarc-project/stats-service

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses>.


.. image:: https://img.shields.io/github/release/monarc-project/stats-service.svg?style=flat-square
  :target: https://github.com/monarc-project/stats-service/releases/latest
  :alt: Latest release

.. image:: https://github.com/monarc-project/stats-service/workflows/Python%20application/badge.svg?style=flat-square
  :target: https://github.com/monarc-project/stats-service/actions?query=workflow%3A%22Python+application%22
  :alt: Workflow

.. image:: https://img.shields.io/github/contributors/monarc-project/stats-service.svg?style=flat-square
  :target: https://github.com/monarc-project/stats-service/graphs/contributors
  :alt: Contributors

.. image:: https://img.shields.io/pypi/v/statsservice.svg?style=flat-square
  :target: https://pypi.org/project/statsservice
  :alt: PyPi version

.. image:: https://img.shields.io/github/license/monarc-project/stats-service.svg?style=flat-square
  :target: https://www.gnu.org/licenses/agpl-3.0.html
  :alt: License AGPLv3

.. image:: https://translate.monarc.lu/widgets/monarc-stats-service/-/svg-badge.svg
  :target: https://translate.monarc.lu/engage/monarc-stats-service/
  :alt: Translate Stats Servie
