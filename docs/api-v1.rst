API v1
======

Endpoints
---------

- /api/v1/organizations/  ``will be removed``
- /api/v1/stats/


.. _section_authentication:

Authentication
--------------

The authentication can be disabled via the configuration file by setting the
value of ``API_KEY_AUTHENTICATION`` to ``False``.

For clarity in the following documentation we will ignore the authentication.

When the authentication is enabled, the client must send a token in the headers
of the request with the key ``X-API-KEY``. Here is an example:


.. code-block:: bash

    $ curl -H "X-API-KEY: SylsDTZTBk2zAkg016vW_aCuO1XQDXPsxrLuI1TG7z5sYvUfRlVf5R4g6kDnLI_o-c5iqrswrWzPANDKXmtV7Q"  http://127.0.0.1:5000/api/v1/stats/
    {"data": [{"uuid": "76a3999f-ab22-4008-a540-f68082f44cb2", "organization": "CASES", "type": "risk", "day": 1, "week": 1, "month": 1, "data": {"what": "you want", "super": "cool"}, "created_at": "2020-05-11T21:56:49.584000", "updated_at": "2020-05-11T21:56:49.584000", "id": "5eb9ca210381f6f321022ae6"}, {"uuid": "66f20692-b627-41e6-8d11-030bd84ee479", "organization": "CASES", "type": "risk", "day": 1, "week": 1, "month": 1, "data": {"what": "you want", "super": "cool"}, "created_at": "2020-05-11T21:57:20.531000", "updated_at": "2020-05-11T21:57:20.531000", "id": "5eb9ca400381f6f321022ae7"}, {"uuid": "e52bbd60-6a99-4e02-bcfd-e454553230f8", "organization": "CASES", "type": "risk", "day": 2, "week": 1, "month": 1, "data": {"what": "you want", "super": "cool"}, "created_at": "2020-05-11T21:57:43.293000", "updated_at": "2020-05-11T21:57:43.293000", "id": "5eb9ca570381f6f321022ae8"}, {"uuid": "b23f081e-e142-4cca-9f43-1e11b4368c9d", "organization": "CASES", "type": "risk", "day": 2, "week": 1, "month": 1, "data": {"what": "you want", "super": "cool"}, "created_at": "2020-05-11T22:00:55.584000", "updated_at": "2020-05-11T22:00:55.584000", "id": "5eb9cb170381f6f321022ae9"}], "has_more": false}


This token enable to identify an organization.


.. code-block:: bash

    $ curl -H "X-API-KEY: BAD-TOKEN"  http://127.0.0.1:5000/api/v1/stats/
    {"error": "Unauthorized"}



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

    $ curl http://127.0.0.1:5000/api/v1/stats/
    {"data": [], "has_more": false}



Create a stat

.. code-block:: bash

    # data is a DynamicField
    # note that we are using the MongoDB id of the created org:
    $ curl -H "Content-Type: application/json" -X POST -d \
    '{"type": "risk", "organization": "CASES", "data": {"what": "you want", "super": "cool"}, "day":1, "week":1, "month":1}' http://127.0.0.1:5000/api/v1/stats/
    {"uuid": "76a3999f-ab22-4008-a540-f68082f44cb2", "organization": "CASES", "type": "risk", "day": 1, "week": 1, "month": 1, "data": {"what": "you want", "super": "cool"}, "created_at": "2020-05-11T21:56:49.584000", "updated_at": "2020-05-11T21:56:49.584000", "id": "5eb9ca210381f6f321022ae6"}



Get the last stat with the id returned previously:

.. code-block:: bash

    $ curl http://127.0.0.1:5000/api/v1/stats/5eb9ca210381f6f321022ae6/
    {"organization": "5ea3717b0cdd5b63ad17b6ce", "type": "risk", "day": 1, "week": 1, "month": 1, "data": {"what": "you want", "super": "cool"}, "created_at": "2020-04-24T23:38:26.326000", "updated_at": "2020-04-24T23:38:26.326000", "id": "5ea378728f826c539837436a"}



You can also use pagination:

.. code-block:: bash

    $ curl http://127.0.0.1:5000/api/v1/stats/?_skip=0&_limit=10




More advanced usage
-------------------

.. _section_stats_api:

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
