import json
import click
import requests

from urllib.parse import urljoin
from statsapi.bootstrap import application

STATS_API_ENDPOINT = urljoin(
    application.config["REMOTE_STATS_SERVER"], "/api/v1/stats/"
)


@application.cli.command("pull-stats")
@click.option("--uuid", default="", help="Organization UUID")
def pull_stats(uuid):
    """Pull stats from an other stats instance for the organization specified
    in parameter.
    """
    r = requests.get(STATS_API_ENDPOINT)
    stats = json.loads(r.content)
    for stat in stats["data"]:
        print(stat)
        # TODO: save the stat
