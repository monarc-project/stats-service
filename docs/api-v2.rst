API v2
======

Endpoints
---------

- /api/v2/organizations/  ``(will be removed)``
- /api/v2/stats/


.. _section_authentication:

Authentication
--------------

When the authentication is enabled, the client must send a token in the headers
of the request with the key ``X-API-KEY``. Here is an example:


.. code-block:: bash

    $ curl -H "X-API-KEY: SylsDTZTBk2zAkg016vW_aCuO1XQDXPsxrLuI1TG7z5sYvUfRlVf5R4g6kDnLI_o-c5iqrswrWzPANDKXmtV7Q"  http://127.0.0.1:5000/api/v2/stats/
    {"data": [{"uuid": "76a3999f-ab22-4008-a540-f68082f44cb2", "anr": 2, "type": "risk", "day": 1, "week": 1, "month": 1, "data": {"what": "you want", "super": "cool"}, "created_at": "2020-05-11T21:56:49.584000", "updated_at": "2020-05-11T21:56:49.584000", "id": "5eb9ca210381f6f321022ae6"}, {"uuid": "66f20692-b627-41e6-8d11-030bd84ee479", "organization": "CASES", "type": "risk", "day": 1, "week": 1, "month": 1, "data": {"what": "you want", "super": "cool"}, "created_at": "2020-05-11T21:57:20.531000", "updated_at": "2020-05-11T21:57:20.531000", "id": "5eb9ca400381f6f321022ae7"}, {"uuid": "e52bbd60-6a99-4e02-bcfd-e454553230f8", "organization": "CASES", "type": "risk", "day": 2, "week": 1, "month": 1, "data": {"what": "you want", "super": "cool"}, "created_at": "2020-05-11T21:57:43.293000", "updated_at": "2020-05-11T21:57:43.293000", "id": "5eb9ca570381f6f321022ae8"}, {"uuid": "b23f081e-e142-4cca-9f43-1e11b4368c9d", "organization": "CASES", "anr": 2, "type": "risk", "day": 2, "week": 1, "month": 1, "data": {"what": "you want", "super": "cool"}, "created_at": "2020-05-11T22:00:55.584000", "updated_at": "2020-05-11T22:00:55.584000", "id": "5eb9cb170381f6f321022ae9"}], "has_more": false}


This token enable to identify an organization.
By default when creating a new organization
(:ref:`section_creating_an_organization`) Stats API will use the
`secrets.token_urlsafe <https://docs.python.org/3/library/secrets.html#secrets.token_urlsafe>`_
function to generate a token. It is possible to specify it manually.


Example of a failed authentication:

.. code-block:: bash

    $ curl -H "X-API-KEY: BAD-TOKEN"  http://127.0.0.1:5000/api/v2/stats/
    {"error": "Unauthorized"}

    $ curl -i -H "X-API-KEY: BAD-TOKEN"  http://127.0.0.1:5000/api/v2/stats/
    HTTP/1.0 401 Unauthorized
    Vary: Accept
    Content-Type: application/json
    Content-Length: 25
    Server: Werkzeug/1.0.1 Python/3.8.0
    Date: Tue, 12 May 2020 21:52:15 GMT

    {"error": "Unauthorized"}


The authentication can be disabled via the configuration file by setting the
value of ``API_KEY_AUTHENTICATION`` to ``False``.

For clarity in the following documentation we will ignore the authentication.


Simple Examples
---------------


Get all organizations

.. code-block:: bash

    $ curl http://127.0.0.1:5000/api/v2/organizations/
    {"data": [], "has_more": false}



Create an organization (let's say with only a token for the moment - same token for the MONARC client/organization):

.. code-block:: bash

    $ curl -H "Content-Type: application/json" -X POST -d \
    '{"name":"CASES","token": "oypvIaGU7uvuJbR4wgYrB7ef1HeXc9sh5g-zrH9WjmHbWHDk3L36lycYEgJevQ9wo-Wv_5PvxNlbIgZTBXVaMw"}' http://127.0.0.1:5000/api/v2/organizations/

This should be done via the dedicated command. This method will be probably removed.



Get all stats

.. code-block:: bash

    $ curl http://127.0.0.1:5000/api/v2/stats/
    {"data": [], "has_more": false}



Create a stat

.. code-block:: bash

    # data is a DynamicField
    # note that we are using the MongoDB id of the created org:
    $ curl -H "Content-Type: application/json" -X POST -d \
    '{"type": "risk", "anr": 2, "data": {"what": "you want", "super": "cool"}, "day":1, "week":1, "month":1}' http://127.0.0.1:5000/api/v2/stats/
    {"uuid": "76a3999f-ab22-4008-a540-f68082f44cb2", "organization": "CASES", "type": "risk", "day": 1, "week": 1, "month": 1, "data": {"what": "you want", "super": "cool"}, "created_at": "2020-05-11T21:56:49.584000", "updated_at": "2020-05-11T21:56:49.584000", "id": "5eb9ca210381f6f321022ae6"}



Get the last stat with the id returned previously:

.. code-block:: bash

    $ curl http://127.0.0.1:5000/api/v2/stats/5eb9ca210381f6f321022ae6/
    {"organization": "5ea3717b0cdd5b63ad17b6ce", "anr": 2, "type": "risk", "day": 1, "week": 1, "month": 1, "data": {"what": "you want", "super": "cool"}, "created_at": "2020-04-24T23:38:26.326000", "updated_at": "2020-04-24T23:38:26.326000", "id": "5ea378728f826c539837436a"}



You can also use pagination:

.. code-block:: bash

    $ curl http://127.0.0.1:5000/api/v2/stats/?_skip=0&_limit=10




More advanced usage
-------------------

.. _section_stats_api:

Stats
~~~~~

Filtering on attributes:

.. code-block:: bash

    $ curl http://127.0.0.1:5000/api/v2/stats/?day=1&month=1


You must be warned that this is a shortcut, the more precise query is:


.. code-block:: bash

    $ curl http://127.0.0.1:5000/api/v2/stats/?day__exact=1&month__exact=1


Getting all stats from the month of February of type *risk* for an organization:

.. code-block:: bash

    $ curl http://127.0.0.1:5000/api/v2/stats/?organization=CASES&type=risk&month=2


Filtering on attributes with methods:

.. code-block:: bash

    $ curl http://127.0.0.1:5000/api/v2/stats/?created_at__gt=2020-05-12T22:29:42.362000

Of course not only ```__gt``` is available. Available methods are:

- todo :-)


.. code-block:: bash

    curl http://127.0.0.1:5000/api/v2/stats/?type=risk&month__gt=2


.. code-block:: bash

    curl http://127.0.0.1:5000/api/v2/stats/?type=risk&month__gt=2&month__lt=8
