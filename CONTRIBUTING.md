You are welcome to contribute to the MONARC Stats Service project.
There are many ways to contribute and participate.

Before starting to contribute please install the Git hook scripts:

```bash
$ git clone https://github.com/monarc-project/stats-service
$ cd stats-service/
$ poetry install
$ pre-commit install
```

Feel free to fork the code, play with it, make some patches and send us the pull
requests.

There is one main branch: what we consider as stable with frequent updates as
hot-fixes.

Features are developed in separated branches and then regularly merged into the
master stable branch.

If your contribution require some documentation changes, a pull-request in order
to update the documentation is strongly recommended. A compiled version of the
documentation is available [here](https://monarc-stats-service.readthedocs.io/).

Please, do not open directly a GitHub issue if you think you have found a
security vulnerability. See our
[vulnerability disclosure](https://www.monarc.lu/community/vulnerability-disclosure/)
page.


## Building the documentation

Please provide documentation when changing, removing, or adding features.
Documentation resides in the project's [docs](docs/) folder.

```bash
$ pip install --upgrade -r requirements-doc.txt
$ make doc
```

It will generate several documentations per tags and development branches.

The documentation is available online
[here](https://www.monarc.lu/documentation/stats-service/).
