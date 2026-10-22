#!/usr/bin/python3
"""Fabric script that generates a .tgz archive from web_static."""
import os
from datetime import datetime
from fabric.api import local, settings


def do_pack():
    """Creates versions/web_static_<YYYYMMDDHHMMSS>.tgz from web_static.

    Returns the archive path if it was generated, otherwise None.
    """
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_path = "versions/web_static_{}.tgz".format(now)

    with settings(warn_only=True):
        if local("mkdir -p versions").failed:
            return None
        print("Packing web_static to {}".format(archive_path))
        if local("tar -cvzf {} web_static".format(archive_path)).failed:
            return None

    size = os.path.getsize(archive_path)
    print("web_static packed: {} -> {}Bytes".format(archive_path, size))
    return archive_path
