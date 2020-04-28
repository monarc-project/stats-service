API v1
======

Endpoints
---------

- /api/v1/organization/
- /api/v1/stats/



Examples
--------


Get all organizations

.. code-block:: bash

    $ curl http://127.0.0.1:5000/api/v1/organization/
    {"data": [], "has_more": false}



Create an organization (let's say with only a token for the moment - same token for the MONARC client/organization):

.. code-block:: bash

    $ curl -H "Content-Type: application/json" -X POST -d \
    '{"token": "UhdSAdTIoBT18r9Fa3W26iN9RRGlknkO62YkWY-yyqn3c_6-hEfIDX0DkF8JvupxfEw"}' http://127.0.0.1:5000/api/v1/organization/



List again the organizations:

.. code-block:: bash

    $ curl http://127.0.0.1:5000/api/v1/organization/
    {"data": [{"token": "UhdSAdTIoBT18r9Fa3W26iN9RRGlknkO62YkWY-yyqn3c_6-hEfIDX0DkF8JvupxfEw", "id": "5ea3717b0cdd5b63ad17b6ce"}], "has_more": false}



Get all stats

.. code-block:: bash

    $ curl -H "AUTHORIZATION: basic <TOKEN>" http://127.0.0.1:5000/api/v1/stats/
    {"data": [], "has_more": false}



Create a stat

.. code-block:: bash

    # data is a DynamicField
    # note that we are using the MongoDB id of the created org:
    $ curl -H "AUTHORIZATION: basic <TOKEN>" -H "Content-Type: application/json" -X POST -d \
    '{"type": "risk", "organization": "5ea3717b0cdd5b63ad17b6ce", "data": {"what": "you want", "super": "cool"}, "day":1, "week":1, "month":1}' http://127.0.0.1:5000/api/v1/stats/
    {"organization": "5ea3717b0cdd5b63ad17b6ce", "type": "risk", "day": 1, "week": 1, "month": 1, "data": {"what": "you want", "super": "cool"}, "created_at": "2020-04-24T23:38:26.326000", "updated_at": "2020-04-24T23:38:26.326000", "id": "5ea378728f826c539837436a"}



Get the last stat with the id returned previously:

.. code-block:: bash

    $ curl -H "AUTHORIZATION: basic <TOKEN>" http://127.0.0.1:5000/api/v1/stats/5ea378728f826c539837436a/
    {"organization": "5ea3717b0cdd5b63ad17b6ce", "type": "risk", "day": 1, "week": 1, "month": 1, "data": {"what": "you want", "super": "cool"}, "created_at": "2020-04-24T23:38:26.326000", "updated_at": "2020-04-24T23:38:26.326000", "id": "5ea378728f826c539837436a"}



Get stats for a specific organization:

.. code-block:: bash

    $ curl -H "AUTHORIZATION: basic UhdSAdTIoBT18r9Fa3W26iN9RRGlknkO62YkWY-yyqn3c_6-hEfIDX0DkF8JvupxfEw"  http://127.0.0.1:5000/api/v1/stats/?organization__exact=5ea3717b0cdd5b63ad17b6ce



You can also use pagination:

.. code-block:: bash

    $ curl http://127.0.0.1:5000/api/v1/stats/?_skip=0&_limit=10
