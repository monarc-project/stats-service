Installation
============

Prerequisites
-------------

Generally speaking, requirements are the following:

- A GNU/Linux distribution (tested on Debian and Ubuntu);
- Python: version >= 3.6.1 and a dependency manager (for example `Poetry <https://python-poetry.org>`_);
- A PostgreSQL server 12.x: persistent storage.


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

    $ sudo apt install python3-pip python3-venv
    $ curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3
    $ echo  'export PATH="$PATH:$HOME/.poetry/bin"' >> ~/.bashrc
    $ . ~/.bashrc

    $ git clone https://github.com/monarc-project/stats-service
    $ cd stats-service/
    $ cp instance/production.py.cfg instance/production.py  # configure appropriately
    $ poetry install # install the application
    $ export STATS_CONFIG=production.py
    $ FLASK_APP=runserver.py poetry run flask db_create # database creation
    $ FLASK_APP=runserver.py poetry run flask db_init # database initialization

    $ FLASK_APP=runserver.py FLASK_ENV=development poetry run flask run


For production you should use `Gunicorn <https://gunicorn.org>`_ or ``mod_wsgi``.
Please read the :ref:`service-management` section.


Check the version:

.. code-block:: bash

    $ curl http://127.0.0.1:5000/about.json
    {
      "api_v1_root": "/api/v1/",
      "version": "v0.1.9 - 05abfe1",
      "version_url": "https://github.com/monarc-project/stats-service/commits/05abfe1"
    }


Install with a script:

.. code-block:: bash

    $ curl -sSL https://raw.githubusercontent.com/monarc-project/stats-service/master/contrib/install.sh | bash


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

Create a new client:

.. code-block:: bash

    heroku run flask client_create --name <name-of-the-client> --role admin

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


.. _service-management:

Service management
------------------

Several solutions are available:

.. contents::
    :local:
    :depth: 1


Daemon
~~~~~~

Whichever way you installed the service, you can choose to use systemd to start
it. Simply create a file ``/etc/systemd/system/statsservice.service`` with the
following contents:

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

You may need to adjust it a bit (for example if you want to use Gunicorn). After adding
this file to your system, you can start the new systemd service with these commands:

.. code-block:: bash

    $ sudo systemctl daemon-reload
    $ sudo systemctl enable statsservice.service
    $ sudo systemctl start statsservice
    $ systemctl status statsservice.service

Accessing logs
``````````````

.. code-block:: bash

    $ journalctl -u statsservice

to follow the logs:

.. code-block:: bash

    $ journalctl -u statsservice -f

mod_wsgi
~~~~~~~~

Create a file ``/etc/apache2/sites-available/statsservice.monarc.lu.conf``
with a content similar to:


.. code-block:: apacheconf

    <VirtualHost *:80>
            ServerName stats.monarc.lu

            ServerAdmin webmaster@localhost
            DocumentRoot /home/monarc/stats-service

            WSGIDaemonProcess statsservice user=www-data group=www-data threads=5 python-home=/home/monarc/.local/share/virtualenvs/statsservice-_tH16p6s/ python-path=/home/monarc/stats-service
            WSGIScriptAlias / /home/monarc/stats-service/webserver.wsgi

            <Directory /home/monarc/stats-service>
                WSGIApplicationGroup %{GLOBAL}
                WSGIProcessGroup statsservice
                WSGIPassAuthorization On

                Options Indexes FollowSymLinks
                Require all granted
            </Directory>

            SetEnv STATS_CONFIG production.py


            # Available loglevels: trace8, ..., trace1, debug, info, notice, warn,
            # error, crit, alert, emerg.
            # It is also possible to configure the loglevel for particular
            # modules, e.g.
            #LogLevel info ssl:warn
            CustomLog /var/log/apache2/stats-service/access.log combined
            ErrorLog /var/log/apache2/stats-service/error.log

            # For most configuration files from conf-available/, which are
            # enabled or disabled at a global level, it is possible to
            # include a line for only one particular virtual host. For example the
            # following line enables the CGI configuration for this host only
            # after it has been globally disabled with "a2disconf".
            #Include conf-available/serve-cgi-bin.conf
    </VirtualHost>


And a file:


.. code-block:: bash

    $ cat stats-service/webserver.wsgi
    #! /usr/bin/env python

    python_home = '/home/monarc/.local/share/virtualenvs/statsservice-_tH16p6s'

    activate_this = python_home + '/bin/activate_this.py'
    with open(activate_this) as file_:
        exec(file_.read(), dict(__file__=activate_this))

    from runserver import application
