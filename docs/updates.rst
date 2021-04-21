Updates
=======

Updating the application consists of performing the following operations:

.. code-block:: bash

    $ cd stats-service/
    $ export FLASK_APP=runserver.py
    $ git pull origin master --tags
    $ poetry install --no-dev
    $ poetry run pybabel compile -d statsservice/translations
    $ poetry run flask db upgrade
    $ sudo systemctl restart statsservice.service


Alternatively you can simply use the provided script:

.. code-block:: bash

    $ ./contrib/update.sh 
    From github.com:monarc-project/stats-service
      * branch            master     -> FETCH_HEAD
    Already up to date.

    > stats-service@0.2.0 postinstall
    > cd statsservice/static/ ; ln -sf ../../node_modules npm_components


    removed 1 package, and audited 7 packages in 877ms

    3 packages are looking for funding
      run `npm fund` for details

    found 0 vulnerabilities
    Installing dependencies from lock file

    No dependencies to install or update

    Installing the current project: statsservice (0.3.0)
    compiling catalog statsservice/translations/fr_FR/LC_MESSAGES/messages.po to statsservice/translations/fr_FR/LC_MESSAGES/messages.mo
    INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
    INFO  [alembic.runtime.migration] Will assume transactional DDL.
    ✨ 🌟 ✨
    Stats Service updated. You can now restart the service. Examples:
        sudo systemctl restart statsservice.service
        sudo systemctl restart apache2.service
