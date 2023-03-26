import os
import urllib.request

from .impl import VERSION_PROVIDERS


def init():
    for prov in VERSION_PROVIDERS.values():
        prov.reload()


def dispense(software: str, major: str, minor: str, directory: str = "."):
    provider = VERSION_PROVIDERS[software]

    url = provider.get_download(major, minor)

    urllib.request.urlretrieve(url, os.path.join(directory, provider.DOWNLOAD_FILE_NAME))

    provider.post_download(directory, major, minor)
