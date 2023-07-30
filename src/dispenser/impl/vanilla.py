import requests

from ..version_base import VersionProvider

URL_VANILLA_GET_VERSIONS = "https://launchermeta.mojang.com/mc/game/version_manifest.json"


class VanillaVersionProvider(VersionProvider):
    """
    the version provider for vanilla snapshot servers
    """
    NAME = "vanilla"

    def __init__(self):
        self.versions = {}

    def reload_from_data(self, data: dict) -> None:
        self.versions = data

    def fetch_data(self) -> dict:
        out = {}

        with requests.Session() as session:
            resp = session.get(URL_VANILLA_GET_VERSIONS).json()

        for v in resp["versions"]:
            if v["type"] not in out:
                out[v["type"]] = {}

            out[v["type"]][v["id"]] = v["url"]

        return out

    def get_major_versions(self):
        return list(self.versions.keys())

    def get_minor_versions(self, major):
        return self.versions.get(major, [])

    def get_download(self, major, minor):
        with requests.Session() as session:
            resp = session.get(self.versions[major][minor]).json()

        url = resp["downloads"]["server"]["url"]
        return url

    def has_version(self, major, minor):
        return major in self.versions and minor in self.versions[major]

    def get_minecraft_version(self, major, minor):
        return minor
