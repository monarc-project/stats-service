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
