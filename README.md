# Stats Service for MONARC

[![Latest release](https://img.shields.io/github/release/monarc-project/stats-service.svg?style=flat-square)](https://github.com/monarc-project/stats-service/releases/latest)
[![License](https://img.shields.io/github/license/monarc-project/stats-service.svg?style=flat-square)](https://www.gnu.org/licenses/agpl-3.0.html)
[![Contributors](https://img.shields.io/github/contributors/monarc-project/stats-service.svg?style=flat-square)](https://github.com/monarc-project/stats-service/graphs/contributors)
[![Workflow](https://github.com/monarc-project/stats-service/workflows/Python%20application/badge.svg?style=flat-square)](https://github.com/monarc-project/stats-service/actions?query=workflow%3A%22Python+application%22)
[![Documentation Status](https://readthedocs.org/projects/monarc-stats-service/badge/?version=latest&style=flat-square)](https://monarc-stats-service.readthedocs.io/en/latest/?badge=latest)
[![PyPi version](https://img.shields.io/pypi/v/statsservice.svg?style=flat-square)](https://pypi.org/project/statsservice)

## Presentation

[This component](https://github.com/monarc-project/stats-service) provides an API
in order to collect statistics from one or several
[MONARC](https://github.com/monarc-project/MonarcAppFO) instances. It can be
deployed just next to MONARC (eventually in a virtual machine) or on a
dedicated server.

These aggregated statistics can then be sent to a central instance.


## Deployment

The following assumes you have already installed ``git``, ``poetry``,  and
``Python >= 3.6.1``.

```bash
$ sudo apt install postgresql
$ git clone https://github.com/monarc-project/stats-service
$ cd stats-service/
$ cp instance/production.py.cfg instance/production.py
$ poetry install
$ poetry shell
$ export FLASK_APP=runserver.py
$ export FLASK_ENV=development
$ export STATS_CONFIG=production.py
$ flask db_create
$ flask db_init

$ flask create_client --name CASES
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


## Documentation

A [documentation is available](https://monarc-stats-service.readthedocs.io).


## Contributors

<!-- contributors starts -->
![Ruslan Baidan](https://avatars0.githubusercontent.com/u/3246171?v=4&s=100)
![README-bot](https://camo.githubusercontent.com/2a16ac7907b6199b1088b020dd0a29b0b380409c/68747470733a2f2f312e67726176617461722e636f6d2f6176617461722f64343366643232633062653861356131323832323461303434633035363363343f643d68747470732533412532462532466769746875622e6769746875626173736574732e636f6d253246696d6167657325324667726176617461727325324667726176617461722d757365722d3432302e706e6726723d67&s=100)
![README-bot](https://camo.githubusercontent.com/2a16ac7907b6199b1088b020dd0a29b0b380409c/68747470733a2f2f312e67726176617461722e636f6d2f6176617461722f64343366643232633062653861356131323832323461303434633035363363343f643d68747470732533412532462532466769746875622e6769746875626173736574732e636f6d253246696d6167657325324667726176617461727325324667726176617461722d757365722d3432302e706e6726723d67&s=100)
![Cédric Bonhomme](https://avatars0.githubusercontent.com/u/465400?v=4&s=100)
<!-- contributors ends -->


## License

[Stats Service](https://github.com/monarc-project/stats-service) is under the
[GNU Affero General Public License version 3](https://www.gnu.org/licenses/agpl-3.0.html).
