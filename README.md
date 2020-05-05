# Stats API for MONARC

[![License](https://img.shields.io/github/license/monarc-project/stats-api.svg?style=flat-square)](https://www.gnu.org/licenses/agpl-3.0.html)
[![Contributors](https://img.shields.io/github/contributors/monarc-project/stats-api.svg?style=flat-square)](https://github.com/monarc-project/stats-api/graphs/contributors)
[![Workflow](https://github.com/monarc-project/stats-api/workflows/Python%20application/badge.svg?style=flat-square)](https://github.com/monarc-project/stats-api/actions?query=workflow%3A%22Python+application%22)
[![Documentation Status](https://readthedocs.org/projects/monarc-stats-api/badge/?version=latest&style=flat-square)](https://monarc-stats-api.readthedocs.io/en/latest/?badge=latest)

## Presentation

Proof of concept for a stats API.

## Deployment

The following assumes you have already installed ``git``, ``poetry``,  and
``Python >= 3.8``.

```bash
$ sudo apt install mongodb
$ git clone https://github.com/monarc-project/stats-api
$ cd stats-api/
$ cp instance/production.py.cfg instance/production.py
$ poetry install
$ poetry shell
$ export FLASK_APP=runserver.py
$ export FLASK_ENV=development
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

A [documentation is available](https://monarc-stats-api.readthedocs.io).


## License

[Stats API](https://github.com/monarc-project/stats-api) is under the
[GNU Affero General Public License version 3](https://www.gnu.org/licenses/agpl-3.0.html).
