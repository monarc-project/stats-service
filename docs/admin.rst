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
