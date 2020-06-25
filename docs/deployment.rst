Deployment
==========

Heroku
------

.. code-block:: bash

    $ git clone https://github.com/monarc-project/stats-service
    $ cd stats-service/
    $ heroku create --region eu <name-of-your-instance>
    $ heroku addons:add heroku-postgresql:hobby-dev
    $ heroku config:set HEROKU=1
    $ heroku config:set INSTANCE_URL=https://<name-of-your-instance>.herokuapp.com
    $ heroku config:set FLASK_APP='runserver.py'
    $ heroku config:set FLASK_ENV='development'
    $ git push heroku master

A demo instance is available
`here <https://monarc-stats-service.herokuapp.com/api/v1/>`_.

Create a new organization:

.. code-block:: bash

    heroku run flask create_organization --name <name-of-the-organization>

All commands (:ref:`cli`) are available. Just prefix with ``heroku run``.


Python Package Index
--------------------

MONARC Stats service is available on `PyPI <https://pypi.org/project/statsservice>`_.


First install and configure PostgreSQL:

.. code-block:: bash

    sudo apt install postgresql


Then install the application:

.. code-block:: bash

    $ curl https://raw.githubusercontent.com/monarc-project/stats-service/master/instance/production.py.cfg -o stats-conf.py
    $ export FLASK_CONFIG=~/stats-conf.py
    $ pipx install statsservice
    $ monarc-stats-service
