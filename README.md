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
$ python app.py
```

Test:

```bash
# Get all stats
$ curl http://0.0.0.0:5000/stats/
{"data": [], "has_more": false}

# Get all organizations
$ curl http://0.0.0.0:5000/organization/
{"data": [], "has_more": false}

# Create an organization (let's say with just a token):
$ curl -H "Content-Type: application/json" -X POST -d \
'{"token": "UhdSAdTIoBT18r9Fa3W26iN9RRGlknkO62YkWY-yyqn3c_6-hEfIDX0DkF8JvupxfEw"}' http://0.0.0.0:5000/organization/


# List again the organizations:
$ curl http://0.0.0.0:5000/organization/
# Result:
{"data": [{"token": "UhdSAdTIoBT18r9Fa3W26iN9RRGlknkO62YkWY-yyqn3c_6-hEfIDX0DkF8JvupxfEw", "id": "5ea3717b0cdd5b63ad17b6ce"}], "has_more": false}


# Create a stat (we could also submit the token in header with -H)
# data is a DynamicField
# note that we are using the MongoDB id of the created org:
$ curl -H "Content-Type: application/json" -X POST -d \
'{"type": "risk", "organization": "5ea3717b0cdd5b63ad17b6ce", "data": {"what": "you want", "super": "cool"}, "day":1, "week":1, "month":1}' http://0.0.0.0:5000/stats/
# Result:
{"organization": "5ea3717b0cdd5b63ad17b6ce", "type": "risk", "day": 1, "week": 1, "month": 1, "data": {"what": "you want", "super": "cool"}, "created_at": "2020-04-24T23:38:26.326000", "updated_at": "2020-04-24T23:38:26.326000", "id": "5ea378728f826c539837436a"}


# Get the last stat with the id returned previously:
$ curl http://0.0.0.0:5000/stats/5ea378728f826c539837436a/
# Result:
{"organization": "5ea3717b0cdd5b63ad17b6ce", "type": "risk", "day": 1, "week": 1, "month": 1, "data": {"what": "you want", "super": "cool"}, "created_at": "2020-04-24T23:38:26.326000", "updated_at": "2020-04-24T23:38:26.326000", "id": "5ea378728f826c539837436a"}
```


For production you can use [Gunicorn](https://gunicorn.org) or ``mod_wsgi``.


## License

[Stats API](https://github.com/monarc-project/stats-api) is under the
[GNU Affero General Public License version 3](https://www.gnu.org/licenses/agpl-3.0.html).
