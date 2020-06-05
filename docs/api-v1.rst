API v1
======

Swagger
-------

https://monarc-stats-service.herokuapp.com/api/v1/swagger.json

Swagger UI: https://monarc-stats-service.herokuapp.com/api/v1


.. literalinclude:: swagger.json
  :language: JSON


Creating a new organization
---------------------------

.. code-block:: bash

    $ curl -X POST "http://127.0.0.1:5000/api/v1/api/v1/organization/" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{  \"name\": \"Company\"}"
    {
      "name": "Company",
      "token": "rddPRk9_t-Z4GOgmY2UL2blKB1DxWB_0yhDlqcsF9p63eXs-oLCdm2c9YgP7cOqGz71GK1tc8lrCenD8AvEr-g"
    }


Getting stats for an organization
---------------------------------

.. code-block:: bash

    $ curl -X GET "http://127.0.0.1:5000/api/v1/api/v1/stats" -H  "accept: application/json" -H  "X-API-KEY: rddPRk9_t-Z4GOgmY2UL2blKB1DxWB_0yhDlqcsF9p63eXs-oLCdm2c9YgP7cOqGz71GK1tc8lrCenD8AvEr-g"
    {
      "metadata": {
        "count": "0",
        "offset": "1",
        "limit": "10"
      },
      "data": []
    }
