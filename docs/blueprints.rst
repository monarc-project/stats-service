Available blueprints
====================

The views of the application are structured in several blueprints.

Blueprints can be enabled or disabled via the configuration variable ``ACTIVE_BLUEPRINTS``.
Example:

.. code-block:: python

    ACTIVE_BLUEPRINTS = ["stats_bp", "admin_bp"]


The blueprint dedicated to the API can not be disabled.


.. toctree::
   :caption: Available blueprints
   :maxdepth: 3
   :hidden:

   api-v1
   root
   map.rst
   stats
   admin
