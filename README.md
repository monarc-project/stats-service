# Stats API for MONARC

## Presentation

Proof of concept for a stats API.

## Deployment

The following assumes you have already installed ``git``, ``poetry``,  and
``Python >= 3.8``.

```bash
$ sudo apt install mongodb
$ git clone https://github.com/monarc-project/stats-api
$ cd stats-api/
$ poetry install
$ poetry shell
$ python runserver.py
```

For production you can use [Gunicorn](https://gunicorn.org) or ``mod_wsgi``.


## License

A [documentation is available](docs) and can be build in HTML or PDF with
Sphinx.


## License

[Stats API](https://github.com/monarc-project/stats-api) is under the
[GNU Affero General Public License version 3](https://www.gnu.org/licenses/agpl-3.0.html).
