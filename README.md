# Stats Service for MONARC

[![License](https://img.shields.io/github/license/monarc-project/stats-service.svg?style=flat-square)](https://www.gnu.org/licenses/agpl-3.0.html)
[![Contributors](https://img.shields.io/github/contributors/monarc-project/stats-service.svg?style=flat-square)](https://github.com/monarc-project/stats-service/graphs/contributors)
[![Workflow](https://github.com/monarc-project/stats-service/workflows/Python%20application/badge.svg?style=flat-square)](https://github.com/monarc-project/stats-service/actions?query=workflow%3A%22Python+application%22)
[![Documentation Status](https://readthedocs.org/projects/monarc-stats-service/badge/?version=latest&style=flat-square)](https://monarc-stats-service.readthedocs.io/en/latest/?badge=latest)

## Presentation

[This component](https://github.com/monarc-project/stats-service) provides an API
in order to collect statistics from one or several
[MONARC](https://github.com/monarc-project/MonarcAppFO) instances. It can be
deployed just next to MONARC (eventually in a virtual machine) or on a
dedicated server.

These aggregated statistics can then be sent to a central instance.


## Deployment

The following assumes you have already installed ``git``, ``poetry``,  and
``Python >= 3.8``.

```bash
$ sudo apt install postgresql
$ git clone https://github.com/monarc-project/stats-service
$ cd stats-service/
$ cp instance/production.py.cfg instance/production.py
$ poetry install
$ poetry shell
$ export FLASK_APP=runserver.py
$ export FLASK_ENV=development
$ flask db_create
$ flask db_init

$ flask create_organization --name CASES
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

For production you can use [Gunicorn](https://gunicorn.org) or ``mod_wsgi``.


## Documentation

A [documentation is available](https://monarc-stats-service.readthedocs.io).


## License

[Stats Service](https://github.com/monarc-project/stats-service) is under the
[GNU Affero General Public License version 3](https://www.gnu.org/licenses/agpl-3.0.html).
