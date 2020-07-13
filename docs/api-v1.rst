API v1
======

Security model
--------------

First, an overview of the security model.


OpenAPI Specification
---------------------

https://monarc-stats-service.herokuapp.com/api/v1/swagger.json

Swagger UI: https://monarc-stats-service.herokuapp.com/api/v1


.. literalinclude:: swagger.json
  :language: JSON


Examples
--------

Getting stats for a client
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    $ curl -X GET "http://127.0.0.1:5000/api/v1/stats" -H  "accept: application/json" -H  "X-API-KEY: rddPRk9_t-Z4GOgmY2UL2blKB1DxWB_0yhDlqcsF9p63eXs-oLCdm2c9YgP7cOqGz71GK1tc8lrCenD8AvEr-g"
    {
      "metadata": {
        "count": "0",
        "offset": "1",
        "limit": "10"
      },
      "data": []
    }
