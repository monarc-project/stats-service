Blueprint admin
===============

Security model
--------------

Clients needs to have an activated account with **admin** permissions and a token in
order to use endpoints of the admin blueprint.


Routes
------

+-------------------------------------+---------+-------------------------------------------------------+---------------------------------------------------------------+
|   Endpoint                          | Methods |    Rule                                               |    Comment                                                    |
+=====================================+=========+=======================================================+===============================================================+
| admin_bp.client_sharing_activate    |  GET    |  /admin/client_sharing_activate.json/<client_uuid>    | Set the attribute is_sharing_enabled of the client to True.   |
+-------------------------------------+---------+-------------------------------------------------------+---------------------------------------------------------------+
| admin_bp.client_sharing_deactivate  |  GET    |  /admin/client_sharing_deactivate.json/<client_uuid>  | Set the attribute is_sharing_enabled of the client to False.  |
+-------------------------------------+---------+-------------------------------------------------------+---------------------------------------------------------------+
| admin_bp.update                     |  GET    |  /admin/update.json                                   | Trigger the update of Stats Service                           |
+-------------------------------------+---------+-------------------------------------------------------+---------------------------------------------------------------+


Examples
--------

Activate the sharing for a client
`````````````````````````````````

.. code-block:: bash

    $ curl -H  "X-API-KEY: 5USubuFK_FXB7fXoMq_Nt0CHRo9SxQW0J_FarVG5fCJmXckz6T1qgE2wtV_aFiGTGvBi1Xr45-CayfgpC-_MMA"  http://127.0.0.1:5000/admin/client_sharing_activate.json/52629c82-f907-47e9-b568-bacc197b750d
    {
        "result": "OK"
    }


Update Stats Service
````````````````````

.. code-block:: bash

    $ curl -H  "X-API-KEY: 5USubuFK_FXB7fXoMq_Nt0CHRo9SxQW0J_FarVG5fCJmXckz6T1qgE2wtV_aFiGTGvBi1Xr45-CayfgpC-_MMA"  http://127.0.0.1:5000/admin/update.json
    {
      "output": "b'Already up to date.\\n'b'\\n'b'> stats-service@0.4.0 postinstall\\n'b'> cd statsservice/static/ ; ln -sf ../../node_modules npm_components\\n'b'\\n'b'\\n'b'added 11 packages, and audited 12 packages in 777ms\\n'b'\\n'b'2 packages are looking for funding\\n'b'  run `npm fund` for details\\n'b'\\n'b'found 0 vulnerabilities\\n'b'Installing dependencies from lock file\\n'b'\\n'b'No dependencies to install or update\\n'b'\\n'b'Installing the current project: statsservice (0.4.0)\\n'b'\\xe2\\x9c\\xa8 \\xf0\\x9f\\x8c\\x9f \\xe2\\x9c\\xa8\\n'b'\\x1b[0;32mStats Service updated. You can now restart the service.\\x1b[0m Examples:\\n'b'    sudo systemctl restart statsservice.service\\n'b'    sudo systemctl restart apache2.service\\n'", 
      "result": "OK"
    }

The output of the
`Shell update script <https://github.com/monarc-project/stats-service/blob/master/contrib/update.sh>`_
for Stats Service is returned.
