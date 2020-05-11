API v1
======

Endpoints
---------

- /api/v1/organizations/
- /api/v1/stats/


Authentication
--------------


Simple Examples
---------------


Get all organizations

.. code-block:: bash

    $ curl http://127.0.0.1:5000/api/v1/organizations/
    {"data": [], "has_more": false}



Create an organization (let's say with only a token for the moment - same token for the MONARC client/organization):

.. code-block:: bash

    $ curl -H "Content-Type: application/json" -X POST -d \
    '{"name":"CASES","token": "oypvIaGU7uvuJbR4wgYrB7ef1HeXc9sh5g-zrH9WjmHbWHDk3L36lycYEgJevQ9wo-Wv_5PvxNlbIgZTBXVaMw"}' http://127.0.0.1:5000/api/v1/organizations/

This should be done via the dedicated command. This method will be probably removed.



Get all stats

.. code-block:: bash

    $ curl -H "AUTHORIZATION: basic <TOKEN>" http://127.0.0.1:5000/api/v1/stats/
    {"data": [], "has_more": false}



Create a stat

.. code-block:: bash

    # data is a DynamicField
    # note that we are using the MongoDB id of the created org:
    $ curl -H "AUTHORIZATION: basic <TOKEN>" -H "Content-Type: application/json" -X POST -d \
    '{"type": "risk", "organization": "CASES", "data": {"what": "you want", "super": "cool"}, "day":1, "week":1, "month":1}' http://127.0.0.1:5000/api/v1/stats/
    {"uuid": "76a3999f-ab22-4008-a540-f68082f44cb2", "organization": "CASES", "type": "risk", "day": 1, "week": 1, "month": 1, "data": {"what": "you want", "super": "cool"}, "created_at": "2020-05-11T21:56:49.584000", "updated_at": "2020-05-11T21:56:49.584000", "id": "5eb9ca210381f6f321022ae6"}



Get the last stat with the id returned previously:

.. code-block:: bash

    $ curl -H "AUTHORIZATION: basic <TOKEN>" http://127.0.0.1:5000/api/v1/stats/5eb9ca210381f6f321022ae6/
    {"organization": "5ea3717b0cdd5b63ad17b6ce", "type": "risk", "day": 1, "week": 1, "month": 1, "data": {"what": "you want", "super": "cool"}, "created_at": "2020-04-24T23:38:26.326000", "updated_at": "2020-04-24T23:38:26.326000", "id": "5ea378728f826c539837436a"}



You can also use pagination:

.. code-block:: bash

    $ curl http://127.0.0.1:5000/api/v1/stats/?_skip=0&_limit=10



More advanced usage
-------------------

Stats
~~~~~

Filtering on attributes:

.. code-block:: bash

    $ curl http://127.0.0.1:5000/api/v1/stats/?day=1&month=1


You must be warned that this is a shortcut, the more precise query is:


.. code-block:: bash

    $ curl http://127.0.0.1:5000/api/v1/stats/?day__exact=1&month__exact=1


Getting all stats from the month of February of type *risk* for an organization:

.. code-block:: bash

    $ curl http://127.0.0.1:5000/api/v1/stats/?organization=CASES&type=risk&month=2
