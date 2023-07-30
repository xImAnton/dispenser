import os
import pathlib
import subprocess
from typing import Optional

import requests

from ..version_base import VersionProvider

URL_FORGE_GET_VERSIONS = "https://files.minecraftforge.net/maven/net/minecraftforge/forge/maven-metadata.json"
URL_FORGE_DOWNLOAD_BUILD = "https://files.minecraftforge.net/maven/net/minecraftforge/forge/{build}/forge-{build}-installer.jar"


class ForgeVersionProvider(VersionProvider):
    """
    the version provider for forge servers
    """
    NAME = "forge"
    DOWNLOAD_FILE_NAME = "installer.jar"

    def __init__(self):
        self.versions = {}

    def has_version(self, major, minor):
        return major in self.versions.keys() and minor in self.versions[major]

    def reload_from_data(self, data: dict) -> None:
        self.versions = data

    def fetch_data(self):
        with requests.Session() as session:
            return session.get(URL_FORGE_GET_VERSIONS).json()

    def get_major_versions(self):
        return list(self.versions.keys())

    def get_minor_versions(self, major):
        if major not in self.versions.keys():
            return []
        return self.versions[major]

    def get_download(self, major, minor):
        return URL_FORGE_DOWNLOAD_BUILD.format(build=minor)

    def post_download(self, directory, major, version):
        subprocess.call(["java", "-jar", "installer.jar", "--installServer"], cwd=directory)
        os.remove(os.path.join(directory, "installer.jar"))

    def get_minecraft_version(self, major, minor):
        return major

    def update_major(self, path: pathlib.Path, new_major: Optional[str] = None):
        raise NotImplemented("forge servers don't support updates yet")

    def update_minor(self, path: pathlib.Path, major: str, new_minor: Optional[str] = None):
        raise NotImplemented("forge servers don't support updates yet")
