
.. _cli:

Command Line Interface
======================


.. _section_creating_an_organization:

Creating an organization
------------------------

.. code-block:: bash

    $ flask create_organization --help
    Usage: flask create_organization [OPTIONS]

      Create an organization.

    Options:
      --name TEXT  Organization name (or UUID)
      --help       Show this message and exit.

Actually an organization name must be specified and is unique.


Example:

.. code-block:: bash

    $ flask create_organization --name CASES
    Name: CASES
    Token: SylsDTZTBk2zAkg016vW_aCuO1XQDXPsxrLuI1TG7z5sYvUfRlVf5R4g6kDnLI_o-c5iqrswrWzPANDKXmtV7Q


Listing organizations
---------------------

.. code-block:: bash

    $ flask list_organizations
    Name: CASES
    Token: xL3F5M-g1HISeAccX_SrYG8ng3vPRbTByhwXIQufkBv1yCLG2eyc7Sl4cOtnDuGFMPQhniIFNIrZ6x-WRi9dNg

    Name: CIRCL
    Token: uJn2zUA361NANAz6dbtstAaAjq3hL28dscxzCjeUOHpIYC87K8nfOAPtRsTGAqT0iwzs7TEgq5DdD0kkwQDhmw


Drop all collections from the database
--------------------------------------

.. code-block:: bash

    $ flask drop_all_collections --help
    Usage: flask drop_all_collections [OPTIONS]

      Drop all collections from the database.

    Options:
      --help  Show this message and exit.


Will ask for confirmation and eventually drop all collections.


Pushing data
------------

Pushing data to a central stats server.

.. code-block:: bash

    $ flask push-stats --help
    Usage: flask push-stats [OPTIONS]

      Push stats for the organization specified in parameter to an other stats
      server.

    Options:
      --name TEXT   Organization name
      --token TEXT  Organization token on remote side
      --help        Show this message and exit.



This command can be executed for example with cron.

The address of the central stats server must be specified in the configuration
file (```instance/production.py```).


Pulling data
------------

Pulling data from a central stats server.
