Updates
=======

Updating the application consists of performing the following operations:

.. code-block:: bash

    $ cd stats-service/
    $ git pull origin master --tags
    $ poetry install
    $ poetry run flask db upgrade
    $ sudo systemctl restart statsservice.service

To date, no database migrations are required.
