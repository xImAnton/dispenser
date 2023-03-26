import os
import subprocess

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
        subprocess.call("java -jar installer.jar --installServer", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=directory)
        files_to_try = [f"forge-{version}-universal.jar", f"forge-{version}.jar"]
        renamed = False
        for file in files_to_try:
            try:
                os.rename(os.path.join(directory, file), os.path.join(directory, "server.jar"))
                renamed = True
                break
            except FileNotFoundError:
                pass
        if not renamed:
            raise FileNotFoundError("couldn't find server file")

    def get_minecraft_version(self, major, minor):
        return major
