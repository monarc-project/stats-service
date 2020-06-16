.. MONARC Stats Service documentation master file, created by
   sphinx-quickstart on Tue Apr 28 15:01:17 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. only:: html

   .. image:: https://readthedocs.org/projects/monarc-stats-service/badge/?version=latest
      :target: https://monarc-stats-service.readthedocs.io/en/latest/?badge=latest
      :alt: Documentation Status

   .. image:: https://github.com/monarc-project/stats-service/workflows/Python%20application/badge.svg?style=flat-square
      :target: https://github.com/monarc-project/stats-service/actions?query=workflow%3A%22Python+application%22
      :alt: Workflow

Presentation
============

`This component <https://github.com/monarc-project/stats-service>`_ provides an API
in order to collect statistics from one or several
`MONARC <https://github.com/monarc-project/MonarcAppFO>`_ instances. It can be
deployed just next to MONARC (eventually in a virtual machine) or on a
dedicated server.

These aggregated statistics can then be sent to a central instance.


Table of contents
=================

.. toctree::
   :maxdepth: 2

   deployment
   api-v1
   stats
   command-line-interface
