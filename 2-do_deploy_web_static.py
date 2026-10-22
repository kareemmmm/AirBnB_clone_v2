#!/usr/bin/python3
"""Fabric script that distributes an archive to the web servers."""
import os
from fabric.api import env, put, run, settings

# Replace with the IP addresses of your web-01 and web-02 servers
env.hosts = ['<IP web-01>', '<IP web-02>']


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
