
.. _cli:

Command Line Interface
======================

In this section commands are presented per categories:

.. contents::
    :local:
    :depth: 1


Database
--------

Creation of the database
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    $ poetry run flask db_create --help
    Usage: flask db_create [OPTIONS]

      Will create the database from configuration parameters.

    Options:
      --help  Show this message and exit.


Initialization of the database
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    $ poetry run flask db_init --help
    Usage: flask db_init [OPTIONS]

      Will initialize the database.

    Options:
      --help  Show this message and exit.


Drop all collections from the database
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    $ flask drop_all_collections --help
    Usage: flask drop_all_collections [OPTIONS]

      Drop all collections from the database.

    Options:
      --help  Show this message and exit.


Will ask for confirmation and eventually drop all collections.



Clients
-------------

Creating an client
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    $ flask create_client --help
    Usage: flask create_client [OPTIONS]

      Create an client.

    Options:
      --name TEXT  Client name (or UUID)
      --help       Show this message and exit.

Actually an client name must be specified and is unique.


Example:

.. code-block:: bash

    $ flask create_client --name CASES
    Name: CASES
    Token: SylsDTZTBk2zAkg016vW_aCuO1XQDXPsxrLuI1TG7z5sYvUfRlVf5R4g6kDnLI_o-c5iqrswrWzPANDKXmtV7Q


Listing clients
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    $ flask list_clients
    Name: CASES
    Token: xL3F5M-g1HISeAccX_SrYG8ng3vPRbTByhwXIQufkBv1yCLG2eyc7Sl4cOtnDuGFMPQhniIFNIrZ6x-WRi9dNg

    Name: CIRCL
    Token: uJn2zUA361NANAz6dbtstAaAjq3hL28dscxzCjeUOHpIYC87K8nfOAPtRsTGAqT0iwzs7TEgq5DdD0kkwQDhmw



Stats
------

Pushing data
~~~~~~~~~~~~

Pushing data to a central stats server.

.. code-block:: bash

    $ flask push-stats --help
    Usage: flask push-stats [OPTIONS]

      Push stats for the client specified in parameter to an other stats
      server.

    Options:
      --name TEXT   Client name
      --token TEXT  Client token on remote side
      --help        Show this message and exit.



This command can be executed for example with cron.

The address of the central stats server must be specified in the configuration
file.


Pulling data
~~~~~~~~~~~~

Pulling data from a central stats server.


Interactions with MOSP
----------------------

.. code-block:: bash

    $ flask is_object_published --help
    Usage: flask is_object_published [OPTIONS]

      Check if an object has been published on MOSP. Returns a boolean.

    Options:
      --uuid TEXT  UUID of the object  [required]
      --help       Show this message and exit.
