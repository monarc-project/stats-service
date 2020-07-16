#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import pathlib
from python_graphql_client import GraphqlClient

root = pathlib.Path(__file__).parent.resolve()
client = GraphqlClient(endpoint="https://api.github.com/graphql")


TOKEN = os.environ.get("CONTRIBUTORS_TOKEN", "")


def replace_chunk(content, marker, chunk):
    r = re.compile(
        r"<!\-\- {} starts \-\->.*<!\-\- {} ends \-\->".format(marker, marker),
        re.DOTALL,
    )
    chunk = "<!-- {} starts -->\n{}\n<!-- {} ends -->".format(marker, chunk, marker)
    return r.sub(chunk, content)


def make_query(after_cursor=None):
    return """
query {
  repository(owner: "monarc-project", name: "stats-service") {
    defaultBranchRef {
      target {
        ... on Commit {
          history {
            totalCount
            edges {
              node {
                ... on Commit {
                  committer {
                    name
                    avatarUrl
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
"""


def fetch_contributors(oauth_token):
    has_next_page = True
    after_cursor = None

    while has_next_page:
        data = client.execute(
            query=make_query(after_cursor),
            headers={"Authorization": "Bearer {}".format(oauth_token)},
        )
        contributors = []
        for node in data["data"]["repository"]["defaultBranchRef"]["target"]["history"][
            "edges"
        ]:
            if node["node"]["committer"]["name"] != "README-bot":
                if not any(
                    d["name"] == node["node"]["committer"]["name"] for d in contributors
                ):
                    contributors.append(node["node"]["committer"])

        has_next_page = False

    return contributors


if __name__ == "__main__":
    readme = root / "README.md"
    contributors = fetch_contributors(TOKEN)

    contributors.sort(key=lambda r: r["name"], reverse=True)
    md = "\n".join(
        [
            "![{name}]({avatarUrl}&s=100)".format(**contributor)
            for contributor in contributors
        ]
    )
    readme_contents = readme.open().read()
    rewritten = replace_chunk(readme_contents, "contributors", md)

    readme.open("w").write(rewritten)
