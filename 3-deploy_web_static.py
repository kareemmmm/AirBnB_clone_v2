#!/usr/bin/python3
"""Fabric script that creates and distributes an archive to the web servers."""
import os
from datetime import datetime
from fabric.api import env, local, put, run, settings

# Replace with the IP addresses of your web-01 and web-02 servers
env.hosts = ['<IP web-01>', '<IP web-02>']

# The archive is created once and reused for every host
archive_path = None


def do_pack():
    """Creates versions/web_static_<YYYYMMDDHHMMSS>.tgz from web_static.

    Returns the archive path if it was generated, otherwise None.
    """
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    path = "versions/web_static_{}.tgz".format(now)

    with settings(warn_only=True):
        if local("mkdir -p versions").failed:
            return None
        print("Packing web_static to {}".format(path))
        if local("tar -cvzf {} web_static".format(path)).failed:
            return None

    print("web_static packed: {} -> {}Bytes".format(
        path, os.path.getsize(path)))
    return path


def do_deploy(archive_path):
    """Deploys the archive_path archive to the web servers.

    Returns True if all operations were done correctly, otherwise False.
    """
    if not os.path.isfile(archive_path):
        return False

    file_name = os.path.basename(archive_path)
    name = file_name.split(".")[0]
    release = "/data/web_static/releases/{}".format(name)
    tmp_file = "/tmp/{}".format(file_name)

    with settings(warn_only=True):
        if put(archive_path, tmp_file).failed:
            return False
        commands = [
            "mkdir -p {}/".format(release),
            "tar -xzf {} -C {}/".format(tmp_file, release),
            "rm {}".format(tmp_file),
            "cp -a {0}/web_static/. {0}/".format(release),
            "rm -rf {}/web_static".format(release),
            "rm -rf /data/web_static/current",
            "ln -s {}/ /data/web_static/current".format(release),
        ]
        for command in commands:
            if run(command).failed:
                return False

    print("New version deployed!")
    return True


def deploy():
    """Creates and distributes an archive to the web servers."""
    global archive_path
    if archive_path is None:
        archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
