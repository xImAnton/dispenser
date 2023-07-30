import requests

from ..version_base import VersionProvider

URL_PAPER_GET_VERSIONS = "https://papermc.io/api/v2/projects/paper/"
URL_PAPER_GET_BUILDS = "https://papermc.io/api/v2/projects/paper/versions/{version}"
URL_PAPER_GET_BUILD_DOWNLOAD = "https://papermc.io/api/v2/projects/paper/versions/{version}/builds/{build}"
URL_PAPER_DOWNLOAD = "https://papermc.io/api/v2/projects/paper/versions/{version}/builds/{build}/downloads/{download}"


class PaperVersionProvider(VersionProvider):
    """
    the version provider for paper servers
    """
    NAME = "paper"

    def __init__(self):
        self.versions = {}

    def has_version(self, major, minor):
        return major in self.versions.keys() and minor in self.versions[major]

    def reload_from_data(self, data: dict) -> None:
        self.versions = data

    def fetch_data(self) -> dict:
        out = {}

        with requests.Session() as session:
            resp = session.get(URL_PAPER_GET_VERSIONS).json()

            for version in resp["versions"]:
                builds = session.get(URL_PAPER_GET_BUILDS.format(version=version)).json()
                out[version] = [str(build) for build in builds["builds"]]

        return out

    def get_download(self, major, minor):
        with requests.Session() as session:
            resp = session.get(URL_PAPER_GET_BUILD_DOWNLOAD.format(version=major, build=minor)).json()

        download = resp["downloads"]["application"]["name"]
        return URL_PAPER_DOWNLOAD.format(version=major, build=minor, download=download)

    def get_major_versions(self):
        return list(self.versions.keys())

    def get_minor_versions(self, major):
        if major not in self.versions.keys():
            return []
        return self.versions[major]

    def get_minecraft_version(self, major, minor):
        return major
