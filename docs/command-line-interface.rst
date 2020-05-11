Command Line Interface
======================

Creating an organization
------------------------

.. code-block:: bash

    $ flask create_organization --help
    Usage: flask create_organization [OPTIONS]

      Create an organization.

    Options:
      --name TEXT  Organization name (or UUID)
      --help       Show this message and exit.

Actually here an organization name must be specified which is unique.
Maybe we should use a UUID instead?


Example:

.. code-block:: bash

    $ flask create_organization --name CASES
    Name: CASES
    Token: SylsDTZTBk2zAkg016vW_aCuO1XQDXPsxrLuI1TG7z5sYvUfRlVf5R4g6kDnLI_o-c5iqrswrWzPANDKXmtV7Q

The token is automatically generated. It will be required when using the
_Stats_ API if the authentication is enabled (for example with basic auth).


TODO: Add a command to update a token (which can be done with the API...)


Drop all collections from the database
--------------------------------------

.. code-block:: bash

    $ flask drop_all_collections --help
    Usage: flask drop_all_collections [OPTIONS]

      Drop all collections from the database.

    Options:
      --help  Show this message and exit.


Will ask for confirmations and eventually drop all collections.


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
