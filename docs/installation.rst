Installation
============

Prerequisites
-------------

Generally speaking, requirements are the following:

- A GNU/Linux distribution (tested on Debian and Ubuntu);
- Python: version >= 3.8 (preferably use `pyenv <https://github.com/pyenv/pyenv>`_)
  and a dependency manager (for example `Poetry <https://python-poetry.org>`_);
- A PostgreSQL server >= 12.x: persistent storage.


Additionally:

- A cron daemon: running scheduled tasks for pushing or pulling stats data.



Deployment
----------

The service can be deployed via several ways:

.. contents::
    :local:
    :depth: 1


From the source
~~~~~~~~~~~~~~~

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
Get the source code and install the software:

.. code-block:: bash

    $ sudo apt install python3-pip python3-venv
    $ curl -sSL https://install.python-poetry.org | python3 -

    $ git clone https://github.com/monarc-project/stats-service
    $ cd stats-service/
    $ npm install
    $ cp instance/production.py.cfg instance/production.py  # configure appropriately
    $ poetry install --no-dev # install the application
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
        "api_v1_root":"/api/v1/",
        "contact":"info@cases.lu",
        "version":"latest",
        "version_url":"https://github.com/monarc-project/stats-service/releases/tag/latest"
    }


Install with a script:

.. code-block:: bash

    $ curl -sSL https://raw.githubusercontent.com/monarc-project/stats-service/master/contrib/install.sh | bash



Docker
~~~~~~

Depending on how you installed Docker on your system, you might have to use ``sudo``,
which is discouraged.

From the repository
```````````````````

.. code-block:: bash

    $ git clone https://github.com/monarc-project/stats-service
    $ cd stats-service/
    $ docker-compose up -d

Stats Service will be available at:
http://127.0.0.1:5000/api/v1

A client should be already created, check:

.. code-block:: bash

    $ docker exec -it statsservice /bin/bash

    root@f31ef9cad854:/statsservice# flask client_list
    UUID: 014ad826-3608-42c2-94d3-4c14cd0702d3
    Name: admin
    Role: 2
    Token: c3ff95aa569afa36f5395317fb77dc300507fe3c
    Sharing Enabled: True
    Created at: 2022-06-30 10:44:17.118606


From the Docker Hub
```````````````````

.. code-block:: bash

    $ docker pull caseslu/statsservice:latest
    $ docker run --name statsservice -d -p 5000:5000 --rm caseslu/statsservice


From the GitHub registry
````````````````````````

.. code-block:: bash

    $ docker pull ghcr.io/monarc-project/stats-service:master
    $ docker run --name statsservice -d -p 5000:5000 --rm docker.pkg.github.com/monarc-project/stats-service/statsservice:master


Ansible with Docker
```````````````````

.. code-block:: yaml

    - name: create statsservice docker network
      docker_network:
        name: "statsservice"
        ipam_config:
        - subnet: "{{ monarc_statsservice_network }}"
      become: True
      tags: stats

    - name: start statsservice database
      docker_container:
        hostname: "statsservice-db"
        name: "statsservice-db"
        image: "postgres:14"
        env:
          POSTGRES_USER: "statsservice"
          POSTGRES_PASSWORD: "statsservice"
          POSTGRES_DB: "statsservice"
        networks:
          - name: "statsservice"
        volumes:
          - "/var/lib/monarc/statsservice-db:/var/lib/postgresql/data"
        state: started
        purge_networks: yes
        restart_policy: always
      become: True
      tags: stats

    - name: start statsservice container
      docker_container:
        hostname: "statsservice"
        name: "statsservice"
        image: "{{ monarc_statsservice_image }}"
        env:
          DB_HOSTNAME: "statsservice-db"
          ADMIN_EMAIL: "{{ emailFrom }}"
          ARMIN_URL: "https://{{ publicHost }}"
          SECRET_KEY: "{{ monarc_statsservice_secret_key }}"
          ADMIN_TOKEN: "{{ monarc_statsservice_admin_token | default(omit) }}"
          DEBUG: "0"
          ENVIRONMENT: "production"
          INSTANCE_URL: "{{ monarc_statsservice_url }}"
          SCRIPT_NAME: "{{ monarc_statsservice_url | urlsplit('path') }}"
          CLIENT_REGISTRATION_OPEN: "1"
        networks:
          - name: "statsservice"
        ports:
          - "0.0.0.0:{{ monarc_statsservice_port }}:5000"
        volumes:
          - "/var/lib/monarc/statsservice-var:/app/var"
        state: started
        purge_networks: yes
        restart_policy: always
      become: True
      tags: stats


From the Python Package Index
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you use this method not all functionalities will be working (some web assets
won't be available), for the moment.

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

In the case you have installed Stats Service from sources,
create a file ``/etc/systemd/system/statsservice.service`` with the following contents:

.. code-block:: ini

    [Unit]
    Description=MONARC Stats service
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


In the case you have installed Stats Service from the Docker registry,
create a file ``/etc/systemd/system/statsservice.service`` with the following contents:

.. code-block:: ini

    [Unit]
    Description=MONARC Stats service
    Requires=docker.service
    After=docker.service

    [Service]
    Type=oneshot
    RemainAfterExit=yes
    WorkingDirectory=/home/monarc/stats-service
    ExecStart=/usr/bin/docker-compose up -d
    ExecStop=/usr/bin/docker-compose down
    TimeoutStartSec=0

    [Install]
    WantedBy=multi-user.target


You may need to adjust your systemd service file. After adding
this file to your system, you can start the new systemd service with these commands:

.. code-block:: bash

    $ sudo systemctl daemon-reload
    $ sudo systemctl enable statsservice.service
    $ sudo systemctl start statsservice
    $ systemctl status statsservice.service


Later, if you want to connect in the container you can do:

.. code-block:: bash

    $ docker exec -it statsservice /bin/bash

    root@f31ef9cad854:/statsservice# flask client_list
    UUID: 014ad826-3608-42c2-94d3-4c14cd0702d3
    Name: admin
    Role: 2
    Token: c3ff95aa569afa36f5395317fb77dc300507fe3c
    Sharing Enabled: True
    Created at: 2022-06-30 10:44:17.118606


Accessing logs
``````````````

.. code-block:: bash

    $ journalctl -u statsservice

to follow the logs:

.. code-block:: bash

    $ journalctl -u statsservice -f


GNU Screen
~~~~~~~~~~

You can simply execute Stats Service in a screen session.

.. code-block:: bash

    $ screen -S statsservice
    $ export STATS_CONFIG=production.py
    $ poetry run python runserver.py
    $ CTRL+a d
    [detached from 183221.statsservice]


Connect to the session:

.. code-block:: bash

    $ screen -ls
    There is a screen on:
            183221.statsservice      (02/25/21 10:56:59)     (Detached)
    1 Socket in /var/run/screen/S-cedric.
    $ screen -xS 183221.statsservice
    $



mod_wsgi Apache module
~~~~~~~~~~~~~~~~~~~~~~

Create a file ``/etc/apache2/sites-available/statsservice.monarc.lu.conf``
with a content similar to:


.. code-block:: apacheconf

    <VirtualHost *:80>
            ServerName dashboard.monarc.lu

            ServerAdmin webmaster@localhost
            DocumentRoot /home/monarc/stats-service

            WSGIDaemonProcess statsservice user=www-data group=www-data threads=5 python-home=/home/ansible/.cache/pypoetry/virtualenvs/statsservice-KKeyDYL6-py3.8 python-path=/var/lib/monarc/stats-service/
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
    </VirtualHost>


And a file:


.. code-block:: bash

    $ cat stats-service/webserver.wsgi
    #! /usr/bin/env python

    python_home = '/home/ansible/.cache/pypoetry/virtualenvs/statsservice-KKeyDYL6-py3.8'

    activate_this = python_home + '/bin/activate_this.py'
    with open(activate_this) as file_:
        exec(file_.read(), dict(__file__=activate_this))

    from runserver import application


Integration with MONARC and collect of the stats
------------------------------------------------

The technical guide of MONARC provides information about the
`integration of Stats Service with MONARC <https://www.monarc.lu/documentation/technical-guide/#stats-service>`_.
Especially related to the configuration of the cron job (which triggers a PHP
command) on the MONARC Front Office. The cron job is responsible for collecting
local statistics and sending those statistics to the Stats Service.
