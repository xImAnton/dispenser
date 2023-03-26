"""
version provider base class
"""
import abc
import time
from typing import List
import os.path
import json

from .util import create_file_if_not_exists


class VersionProvider(abc.ABC):
    """
    the base class for a version provider
    A version provider is responsible for delivering and downloading all available versions for a specific server software and its addons
    """
    NAME = "version provider"
    DOWNLOAD_FILE_NAME = "server.jar"
    CACHE_TIME = 7200

    def reload(self, force: bool = False) -> None:
        """
        reloads the version provider from cache or newly fetched data
        """
        data_file = os.path.join("cache", "versions", self.NAME + ".json")
        create_file_if_not_exists(data_file, "{}")

        with open(data_file, "r") as f:
            data = json.loads(f.read())

        if ((data.get("$time") or 0) + self.CACHE_TIME < int(time.time())) or force:
            data = self.fetch_data()
            data["$time"] = int(time.time())

            with open(data_file, "w") as f:
                f.write(json.dumps(data))

        self.reload_from_data(data)

    @abc.abstractmethod
    def fetch_data(self) -> dict:
        """
        should fetch all versions and return them in a data structure to be cached
        :return:
        """
        return {}

    @abc.abstractmethod
    def reload_from_data(self, data: dict) -> None:
        pass

    @abc.abstractmethod
    def has_version(self, major: str, minor: str) -> bool:
        """
        should check whether the specific version is valid
        :return: True if the version can be downloaded, False if not
        """
        return False

    @abc.abstractmethod
    def get_download(self, major: str, minor: str) -> str:
        """
        should return the download url for the specified version
        :return: the url which can be used to download the jar for the specified version
        """
        return "//"

    def post_download(self, directory: str, major: str, minor: str):
        """
        optional cleanup/ file modification/ installation after download
        :param directory: the directory where the jar was downloaded to
        :param major: the installed major version
        :param minor: the installed minor version
        """
        pass

    @abc.abstractmethod
    def get_major_versions(self) -> List[str]:
        """
        should return all major versions available for this software
        :return: a list major version identifier strings
        """
        return []

    @abc.abstractmethod
    def get_minor_versions(self, major: str) -> List[str]:
        """
        should return all minor versions for the specified major version
        :return: a list of all minor versions for the major version
        """
        return []

    @abc.abstractmethod
    def get_minecraft_version(self, major: str, minor: str) -> str:
        """
        should return the minecraft client version of a specific version
        :return: the minecraft version as string. example: "1.17.1"
        """
        return ""
