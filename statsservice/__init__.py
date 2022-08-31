#! /usr/bin/env python
import importlib
import os
import subprocess

from statsservice.bootstrap import application

BASE_DIR = os.path.dirname(application.instance_path)


def get_version() -> str:
    """Get the current version of the software. First it checks if the environment
    variable ``STATSSERVICE_VERSION`` is defined. If not, if a .git folder is present
    it uses ``Git tags``, else it uses ``importlib`` module."""
    if os.getenv("STATSSERVICE_VERSION"):
        return os.getenv("STATSSERVICE_VERSION", "")

    version = (
        subprocess.run(
            ["git", "-C", BASE_DIR, "describe", "--tags"],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
        .stdout.decode()
        .strip()
    ) or ""
    if not version:
        try:
            version = "v" + importlib.metadata.version("statsservice")
        except importlib.metadata.PackageNotFoundError:
            version = ""
    return version


__version__ = get_version()
