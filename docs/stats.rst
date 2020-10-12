Blueprint stats
===============

The goal of this blueprint is to return formatted custom stats. It is in
read-only mode with only public routes (no authentication required).

Endpoints
---------

- /stats. At that time this route simply returns a HTML file. Some charts can be
  displayed for example with the data from the following routes.
- /stats/threats.json
- /stats/vulnerabilities.json
- /stats/risks.json


Threats
```````

.. code-block:: bash

    $ curl http://127.0.0.1:5000/stats/threats.json?processor=threat_average_on_date&days=100
    {
      "b402d4e0-4576-11e9-9173-0800277f0571": {
        "2020-07-13": {
          "averageRate": 2.32,
          "count": 10.0,
          "maxRisk": 35.5
        },
        "2020-07-14": {
          "averageRate": 3.0,
          "count": 8.0,
          "maxRisk": 34.0
        },
        "2020-07-27": {
          "averageRate": 3.0,
          "count": 8.0,
          "maxRisk": 34.0
        },
        "2020-07-28": {
          "averageRate": 2.82,
          "count": 12.0,
          "maxRisk": 36.0
        },
        "2020-07-29": {
          "averageRate": 3.0,
          "count": 8.0,
          "maxRisk": 34.0
        },
        "2020-07-31": {
          "averageRate": 2.82,
          "count": 6.0,
          "maxRisk": 36.0
        }
      },
      "b402d523-4576-11e9-9173-0800277f0571": {
        "2020-07-13": {
          "averageRate": 2.87,
          "count": 8.0,
          "maxRisk": 45.0
        },
        "2020-07-14": {
          "averageRate": 2.87,
          "count": 8.0,
          "maxRisk": 45.0
        },
        ...
      }
      ...
    }


- if the parameter ``days`` is not specified the default value is 365.
- ``threat_average_on_date`` is also the default processor.


Vulnerabilities
```````````````

.. code-block:: bash

    $ curl http://127.0.0.1:5000/stats/vulnerabilities.json?processor=vulnerability_average_on_date&days=100
    {
      "69fbfe14-4591-11e9-9173-0800277f0571": {
        "2020-08-01": {
          "averageRate": 2.0,
          "count": 3.0,
          "maxRisk": 18.0
        },
        "2020-08-03": {
          "averageRate": 2.0,
          "count": 3.0,
          "maxRisk": 18.0
        }
      },
      "69fbfe5f-4591-11e9-9173-0800277f0571": {
        "2020-08-01": {
          "averageRate": 1.0,
          "count": 1.0,
          "maxRisk": 6.0
          },
          ...
        }
        ...
      }


Risks
`````

.. code-block:: bash

    $ curl http://127.0.0.1:5000/stats/risks.json?processor=risk_averages_on_date
    {
      "current": {
        "informational": {
          "High risks": {
            "2020-10-01": 8.0, 
            "2020-10-12": 8.0
          }, 
          "Low risks": {
            "2020-10-01": 66.0, 
            "2020-10-12": 12.0
          }, 
          "Medium risks": {
            "2020-10-01": 27.0, 
            "2020-10-12": 27.0
          }
        }, 
        "operational": {
          "High risks": {
            "2020-10-01": 10.0, 
            "2020-10-12": 10.0
          }, 
          "Low risks": {
            "2020-10-01": 18.0, 
            "2020-10-12": 18.0
          }, 
          "Medium risks": {
            "2020-10-01": 0.0, 
            "2020-10-12": 0.0
          }
        }
      }, 
      "residual": {
        "informational": {
          "High risks": {
            "2020-10-01": 1.0, 
            "2020-10-12": 1.0
          }, 
          "Low risks": {
            "2020-10-01": 74.0, 
            "2020-10-12": 74.0
          }, 
          "Medium risks": {
            "2020-10-01": 26.0, 
            "2020-10-12": 26.0
          }
        }, 
        "operational": {
          "High risks": {
            "2020-10-01": 0.0, 
            "2020-10-12": 0.0
          }, 
          "Low risks": {
            "2020-10-01": 28.0, 
            "2020-10-12": 28.0
          }, 
          "Medium risks": {
            "2020-10-01": 0.0, 
            "2020-10-12": 0.0
          }
        }
      }
    }


.. code-block:: bash

    $ curl http://127.0.0.1:5000/stats/risks.json?processor=risk_averages
    {
      "current": {
        "informational": {
          "High risks": 8.0, 
          "Low risks": 30.0, 
          "Medium risks": 27.0
        }, 
        "operational": {
          "High risks": 10.0, 
          "Low risks": 18.0, 
          "Medium risks": 0.0
        }
      }, 
      "residual": {
        "informational": {
          "High risks": 1.0, 
          "Low risks": 74.0, 
          "Medium risks": 26.0
        }, 
        "operational": {
          "High risks": 0.0, 
          "Low risks": 28.0, 
          "Medium risks": 0.0
        }
      }
    }
