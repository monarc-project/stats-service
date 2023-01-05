# Stats Service for MONARC

[![Latest release](https://img.shields.io/github/release/monarc-project/stats-service.svg?style=flat-square)](https://github.com/monarc-project/stats-service/releases/latest)
[![License](https://img.shields.io/github/license/monarc-project/stats-service.svg?style=flat-square)](https://www.gnu.org/licenses/agpl-3.0.html)
[![Contributors](https://img.shields.io/github/contributors/monarc-project/stats-service.svg?style=flat-square)](https://github.com/monarc-project/stats-service/graphs/contributors)
[![Workflow](https://github.com/monarc-project/stats-service/workflows/Python%20application/badge.svg?style=flat-square)](https://github.com/monarc-project/stats-service/actions?query=workflow%3A%22Python+application%22)
[![CodeQL](https://github.com/monarc-project/stats-service/workflows/CodeQL/badge.svg?style=flat-square)](https://github.com/monarc-project/stats-service/actions?query=workflow%3A%22CodeQL%22)
[![Translation status](https://translate.monarc.lu/widgets/monarc-stats-service/-/svg-badge.svg)](https://translate.monarc.lu/engage/monarc-stats-service/)
[![PyPi version](https://img.shields.io/pypi/v/statsservice.svg?style=flat-square)](https://pypi.org/project/statsservice)

## Presentation

[MONARC Stats Service](https://github.com/monarc-project/stats-service) is a libre
software which is providing:

* an API in order to **collect** statistics from one or several
  [MONARC](https://github.com/monarc-project/MonarcAppFO) instances and to **return**
  these statistics with different filters and aggregation methods;
* a dashboard that summarizes the **current cybersecurity landscape**. The charts are
  based on the statistics collected.

This software can be deployed just next to a MONARC instance or on a dedicated server.

The collected statistics can be sent to an other Stats Service instance.

The public official instance operated by [NC3-LU](https://www.nc3.lu) is
available at [https://dashboard.monarc.lu](https://dashboard.monarc.lu).


## Documentation

To be found in the ``docs`` directory of the source code, or
viewed online [here](https://www.monarc.lu/documentation/stats-service/).

Several
[installation](https://www.monarc.lu/documentation/stats-service/master/installation.html)
ways and the
[update](https://www.monarc.lu/documentation/stats-service/master/updates.html)
procedure are described.


## Quick deployment

```bash
$ git clone https://github.com/monarc-project/stats-service
$ cd stats-service/
$ docker-compose up -d
```

Stats Service will be available at:
http://127.0.0.1:5000/api/v1

More information in the
[installation section](https://www.monarc.lu/documentation/stats-service/master/installation.html)
of the documentation.


## License

[Stats Service](https://github.com/monarc-project/stats-service) is under the
[GNU Affero General Public License version 3](https://www.gnu.org/licenses/agpl-3.0.html).
