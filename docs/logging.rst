Logging
=======

Format of the log messages:

.. code-block:: python

    log_format="%(asctime)s %(levelname)s %(name)s %(funcName)s %(lineno)s: %(message)s"


Example:

.. code-block:: bash

    2020-09-02 11:19:43,894 ERROR statsservice.api.v1.stats post 248: Duplicate stats: fecea306-2b0e-4129-b34d-2a8876b1fede


You can define the path of the log file in the configuration file. The default is
``./var/stats.log``. If not specified ``sys.stderr`` will be used.


Modules with logging
--------------------

- statsservice.api.v1.client
- statsservice.api.v1.stats
