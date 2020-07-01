Deployment
==========

MONARC Stats service can be deployed via several ways:

.. contents::
    :local:


From the source
---------------

.. code-block:: bash

    $ sudo apt install postgresql
    $ git clone https://github.com/monarc-project/stats-service
    $ cd stats-service/
    $ cp instance/production.py.cfg instance/production.py
    $ poetry install
    $ poetry shell
    $ export FLASK_APP=runserver.py
    $ export FLASK_ENV=development
    $ flask db_create
    $ flask db_init



To Heroku
---------

You can use this button:

.. image:: https://www.herokucdn.com/deploy/button.png
   :target: https://heroku.com/deploy?template=https://github.com/CASES-LU/MOSP
   :alt: Documentation Status

or via command line:

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



From the Python Package Index
-----------------------------

.. image:: https://img.shields.io/pypi/v/statsservice.svg?style=flat-square
   :target: https://pypi.org/project/statsservice
   :alt: PyPi version

MONARC Stats service is available on `PyPI <https://pypi.org/project/statsservice>`_.


First install and configure PostgreSQL:

.. code-block:: bash

    sudo apt install postgresql


Then install the application:

.. code-block:: bash

    $ pipx install statsservice
    $ monarc-stats-service
     * Serving Flask app "statsservice.bootstrap" (lazy loading)
     * Environment: production
     * Debug mode: off
     * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)


If you want to use a custom configuration file:

.. code-block:: bash

    $ curl https://raw.githubusercontent.com/monarc-project/stats-service/master/instance/production.py.cfg -o production.py
    $ export STATS_CONFIG=~/production.py
