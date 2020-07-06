Installation
============

Prerequisites
-------------

Generally speaking, requirements are the following:

- A GNU/Linux distribution (tested on Debian and Ubuntu);
- Python: version >= 3.8 and a dependency manager (for example `Poetry <https://python-poetry.org>`_);
- A PostgreSQL server 12.x: persistent storage;


Additionally:

- A cron daemon: running scheduled tasks for pushing or pulling stats data.


Creation of a PostgreSQL user:

.. code-block:: bash

    $ sudo apt install postgresql
    $ sudo -u postgres createuser <username>
    $ sudo -u postgres psql
    psql (11.2 (Ubuntu 11.2-1))
    Type "help" for help.
    postgres=# ALTER USER <username> WITH encrypted password '<password>';
    postgres=# ALTER USER <username> WITH SUPERUSER;
    ALTER ROLE
    postgres-# \q

The user name and password chosen must be specified later in the configuration file.



Deployment
----------

The service can be deployed via several ways:

.. contents::
    :local:
    :depth: 1


From the source
~~~~~~~~~~~~~~~

.. code-block:: bash

    $ git clone https://github.com/monarc-project/stats-service
    $ cd stats-service/
    $ cp instance/production.py.cfg instance/production.py
    $ poetry install
    $ poetry shell
    $ export FLASK_APP=runserver.py
    $ export FLASK_ENV=development
    $ flask db_create
    $ flask db_init

For production you can use `Gunicorn <https://gunicorn.org>`_ or ``mod_wsgi``.


To Heroku
~~~~~~~~~

You can use this button:

.. image:: https://www.herokucdn.com/deploy/button.png
   :target: https://heroku.com/deploy?template=https://github.com/monarc-project/stats-service
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
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. only:: html

    .. image:: https://img.shields.io/pypi/v/statsservice.svg?style=flat-square
       :target: https://pypi.org/project/statsservice
       :alt: PyPi version

MONARC Stats service is available on `PyPI <https://pypi.org/project/statsservice>`_.


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



With systemd
~~~~~~~~~~~~

Get the code and configure the application
``````````````````````````````````````````

.. code-block:: bash

    $ sudo apt install make build-essential libssl-dev zlib1g-dev libbz2-dev \
    libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
    xz-utils tk-dev libffi-dev liblzma-dev python-openssl python3-pip python3-venv

    $ curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3

    $ echo  'export PATH="$PATH:$HOME/.poetry/bin"' >> ~/.bashrc 
    $ . ~/.bashrc
    $
    $ git clone https://github.com/monarc-project/stats-service
    $ cd stats-service/
    $ cp instance/production.py.cfg instance/production.py  # configure appropriately
    $ poetry install # install the application
    $ FLASK_APP=runserver.py poetry run flask db_create # database creation
    $ FLASK_APP=runserver.py poetry run flask db_init # database initialization

Write a systemd configuration file
``````````````````````````````````

Create the file ``/etc/systemd/system/statsservice.service`` with the following contents:

.. code-block:: ini

    [Unit]
    Description=Stats
    After=network.target

    [Service]
    User=monarc
    Environment=FLASK_APP=runserver.py
    Environment=FLASK_ENV=production
    Environment=STATS_CONFIG=production.py
    WorkingDirectory=/home/monarc/stats-service
    ExecStart=/home/monarc/.poetry/bin/poetry run flask run
    Restart=always


    [Install]
    WantedBy=multi-user.target


After adding this file to your system, you can start the service with these commands:

.. code-block:: bash

    $ sudo systemctl daemon-reload
    $ sudo systemctl enable statsservice.service
    $ sudo systemctl start statsservice
    $ systemctl status statsservice.service

Accessing logs
``````````````

.. code-block:: bash

    $ journalctl -u statsservice
