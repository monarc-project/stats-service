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

The public official instance operated by [CASES](https://www.cases.lu) is
available at [https://dashboard.monarc.lu](https://dashboard.monarc.lu).


## Documentation

To be found in the ``docs`` directory of the source code, or
viewed online [here](https://www.monarc.lu/documentation/stats-service/).

Several
[installation](https://www.monarc.lu/documentation/stats-service/master/installation.html)
ways are described.

The
[update procedure](https://www.monarc.lu/documentation/stats-service/master/updates.html)
is also described.


## Quick deployment

The following assumes you have already installed ``git``, ``poetry``,  and
``Python >= 3.8``.

```bash
$ sudo apt install postgresql
$ git clone https://github.com/monarc-project/stats-service
$ cd stats-service/
$ npm install
$ cp instance/production.py.cfg instance/production.py
$ poetry install --no-dev
$ poetry shell
$ pybabel compile -d statsservice/translations
$ export FLASK_APP=runserver.py
$ export FLASK_ENV=development
$ export STATS_CONFIG=production.py
$ flask db_create
$ flask db_init
$ flask db upgrade

$ flask client_create --name CASES
Name: CASES
Token: SylsDTZTBk2zAkg016vW_aCuO1XQDXPsxrLuI1TG7z5sYvUfRlVf5R4g6kDnLI_o-c5iqrswrWzPANDKXmtV7Q
Created at: 2020-06-16 14:25:32.947745

$ flask run
 * Serving Flask app "runserver.py" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 268-178-811
```

or use the [docker image](https://hub.docker.com/r/caseslu/statsservice).



## License

[Stats Service](https://github.com/monarc-project/stats-service) is under the
[GNU Affero General Public License version 3](https://www.gnu.org/licenses/agpl-3.0.html).
