Command Line Interface
======================

Pushing data
------------

Pushing data to a central stats server.

.. code-block:: bash

    $ flask push-stats --help
    Usage: flask push-stats [OPTIONS]

      Push stats for the organization specified in parameter to an other stats
      server.

    Options:
      --uuid TEXT  Organization UUID
      --help       Show this message and exit.

This command can be executed for example with cron.

The address of the central stats server must be specified in the configuration
file (```instance/production.py```).


Pulling data
------------

Pulling data from a central stats server.
