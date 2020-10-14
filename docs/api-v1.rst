API v1
======

Blueprint dedicated to the main API. It is composed of two namespaces, *client* and
*stats*, that are used for the endpoints ``api/v1/stats`` and ``api/v1/client``.

New namespaces are easily plugable via the file: ``api/v1/__init__.py``.


Security model
--------------

First, an overview of the security model. Section to be completed.


OpenAPI Specification
---------------------


.. literalinclude:: swagger.json
  :language: JSON


Detailed examples with the API
------------------------------

Getting stats for a client
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    $ curl -X GET "http://127.0.0.1:5000/api/v1/stats" -H  "accept: application/json" -H  "X-API-KEY: rddPRk9_t-Z4GOgmY2UL2blKB1DxWB_0yhDlqcsF9p63eXs-oLCdm2c9YgP7cOqGz71GK1tc8lrCenD8AvEr-g"
    {
      "metadata": {
        "count": "0",
        "offset": "0",
        "limit": "0"
      },
      "data": []
    }


Invoking a processor
~~~~~~~~~~~~~~~~~~~~

Processors are utilities to process stats data. Processors are currently defined in
``statsservice/lib/processors.py``. They operate on different kind of stats:

- risks;
- threats;
- vulnerabilities.

They can do a lot of things, like evaluate different averages based on user
requirements. The result of the processor is sent in the response from the API.

You can get the list of available processors:

.. code-block:: bash

    $ curl http://127.0.0.1:5000/api/v1/stats/processed/list
    [
        {
            "name": "risk_averages",
            "description": "Evaluates the averages for the risks. Averages are evaluated per categories\n    (current/residual, informational/operational, low/medium/high)."
        },
        {
            "name": "risk_averages_on_date",
            "description": "Evaluates the averages for the risks per date. Averages are evaluated per categories\n    (current/residual, informational/operational, low/medium/high).\n    Supported parameters:\n    - risks_type: informational or residual\n    - risk_state: current or residual."
        },
        {
            "name": "threat_average_on_date",
            "description": "Aggregation and average of threats per date for each threat (accross all risk\n    analysis).\n    "
        },
        {
            "name": "vulnerability_average_on_date",
            "description": "Aggregation and average of vulnerabilities per date for each vulnerability\n    (accross all risk analysis).\n    "
        }
    ]


Some processors can use dedicated parameters. For this purpose the parameter
``processor_params`` can be used to transfer some parameters directly to a processor.

For example you might want to call the processor ``risk_averages_on_date`` but you want
that this processor only evaluates the averages for residual risks that are also
operational risks (and not informational). The request will look like:

.. code-block:: bash

    curl -X GET "http://127.0.0.1:5000/api/v1/stats/processed/" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{  \"type\": \"risk\",  \"processor\": \"risk_averages_on_date\",  \"local_stats_only\": 0, \"date_from\":\"2020-06-12\",\"processor_params\": {\"risks_type\":\"operational\",\"risks_state\":\"residual\"}}"


Internally the processor ``processor_params`` will honor the value provided with
the parameters ``risks_type`` and ``risk_state``.

- ``risk_type`` can be *informational* or *operational*;
- ``risk_state`` can be *current* or *residual*.


Generally, you can get information about a processor:


.. code-block:: bash

    $ echo -e `curl -s http://127.0.0.1:5000/api/v1/stats/processed/list | jq '.[] | select(.name=="risk_averages_on_date") | .description'`
    "Evaluates the averages for the risks per date. Averages are evaluated per categories
     (current/residual, informational/operational, low/medium/high).
     Supported parameters:
     - risks_type: informational or operational
     - risk_state: current or residual."
