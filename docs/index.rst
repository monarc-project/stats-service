.. MONARC Stats Service documentation master file, created by
   sphinx-quickstart on Tue Apr 28 15:01:17 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. only:: html

   .. image:: https://img.shields.io/github/release/monarc-project/stats-service.svg?style=flat-square
      :target: https://github.com/monarc-project/stats-service/releases/latest
      :alt: Latest release

   .. image:: https://readthedocs.org/projects/monarc-stats-service/badge/?version=latest
      :target: https://monarc-stats-service.readthedocs.io/en/latest/?badge=latest
      :alt: Documentation Status

   .. image:: https://github.com/monarc-project/stats-service/workflows/Python%20application/badge.svg?style=flat-square
      :target: https://github.com/monarc-project/stats-service/actions?query=workflow%3A%22Python+application%22
      :alt: Workflow

   .. image:: https://img.shields.io/github/contributors/monarc-project/stats-service.svg?style=flat-square
      :target: https://github.com/monarc-project/stats-service/graphs/contributors
      :alt: Contributors

   .. image:: https://img.shields.io/pypi/v/statsservice.svg?style=flat-square
      :target: https://pypi.org/project/statsservice
      :alt: PyPi version


.. |br| raw:: html

  <br />


.. raw:: latex

  \clearpage

Presentation
============

`This component <https://github.com/monarc-project/stats-service>`_ provides an
API in order to **collect** statistics from one or several
`MONARC <https://github.com/monarc-project/MonarcAppFO>`_ instances and to
**return** these statistics with different filters and aggregation methods. |br| Charts
from the collected statistics are also available.

The MONARC Stats Service can be deployed just next to a MONARC instance or on a
dedicated server.

The collected statistics can be sent to an other stats instance.


Technical considerations
------------------------

.. toctree::
   :maxdepth: 3

   installation
   updates
   command-line-interface
   logging


Conceptual considerations
-------------------------

.. toctree::
   :maxdepth: 3

   architecture


Blueprints
----------

.. toctree::
   :maxdepth: 3

   api-v1
   stats


License
=======

MONARC Stats Service is licensed under
`GNU Affero General Public License version 3 <https://www.gnu.org/licenses/agpl-3.0.html>`_.


* Copyright (C) 2020-2021 Cédric Bonhomme
* Copyright (C) 2020-2021 SECURITYMADEIN.LU
