Blueprint stats
===============

The goal of this blueprint is to return formatted custom stats. It is in
read-only mode with only public routes (no authentication required).

Endpoints
---------

- /stats - The only view of this blueprint which is supposed to return a HTML file.
- /stats/risks.json
- /stats/threats.json


Threats
```````


.. code-block:: bash

    $ curl http://127.0.0.1:5000/stats/threats.json?days=2
    {
      "b402d4e0-4576-11e9-9173-0800277f0571": {
        "count": 10.0,
        "maxRisk": 35.0
      },
      "b402d523-4576-11e9-9173-0800277f0571": {
        "count": 8.0,
        "maxRisk": 45.0
      },
      "b402d530-4576-11e9-9173-0800277f0571": {
        "count": 6.0,
        "maxRisk": 45.0
      },
      "b402d557-4576-11e9-9173-0800277f0571": {
        "averageRate": 5.5,
        "count": 1.0,
        "maxRisk": 1.0
      },
      "b402d563-4576-11e9-9173-0800277f0571": {
        "averageRate": 5.5,
        "count": 1.0,
        "maxRisk": 1.0
      },
      "b402d579-4576-11e9-9173-0800277f0571": {
        "count": 2.0,
        "maxRisk": 3.0
      },
      "b402d584-4576-11e9-9173-0800277f0571": {
        "count": 2.0,
        "maxRisk": 2.0
      },
      "b402d58f-4576-11e9-9173-0800277f0571": {
        "count": 4.0,
        "maxRisk": 27.0
      },
      "b402d5af-4576-11e9-9173-0800277f0571": {
        "count": 7.0,
        "maxRisk": 20.0
      },
      "b402d5c9-4576-11e9-9173-0800277f0571": {
        "count": 2.0,
        "maxRisk": 2.0
      },
      "b402d5d5-4576-11e9-9173-0800277f0571": {
        "count": 3.0,
        "maxRisk": 18.0
      },
      "b402d5ea-4576-11e9-9173-0800277f0571": {
        "count": 4.0,
        "maxRisk": 30.0
      },
      "b402d600-4576-11e9-9173-0800277f0571": {
        "count": 2.0,
        "maxRisk": 6.0
      },
      "b402d60a-4576-11e9-9173-0800277f0571": {
        "count": 4.0,
        "maxRisk": 12.0
      },
      "b402d615-4576-11e9-9173-0800277f0571": {
        "count": 3.0,
        "maxRisk": 30.0
      },
      "b402d620-4576-11e9-9173-0800277f0571": {
        "count": 2.0,
        "maxRisk": 6.0
      },
      "b402d63d-4576-11e9-9173-0800277f0571": {
        "count": 2.0,
        "maxRisk": 3.0
      },
      "b402d648-4576-11e9-9173-0800277f0571": {
        "averageRate": 5.5,
        "count": 1.0,
        "maxRisk": 3.0
      },
      "b402d653-4576-11e9-9173-0800277f0571": {
        "averageRate": 5.5,
        "count": 1.0,
        "maxRisk": 3.0
      },
      "b402d673-4576-11e9-9173-0800277f0571": {
        "count": 2.0,
        "maxRisk": 6.0
      },
      "b402d67d-4576-11e9-9173-0800277f0571": {
        "count": 2.0,
        "maxRisk": 12.0
      },
      "b402d688-4576-11e9-9173-0800277f0571": {
        "averageRate": 5.5,
        "count": 1.0,
        "maxRisk": 3.0
      }
    }
