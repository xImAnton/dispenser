import pathlib
from typing import Optional

from .impl import VERSION_PROVIDERS


def update_major(software: str, path: str, to: Optional[str] = None) -> tuple[str, str, str]:
    provider = VERSION_PROVIDERS[software]

    major, minor = provider.update_major(pathlib.Path(path), to)

    return provider.NAME, major, minor


def update_minor(software: str, path: str, major: str, to: Optional[str] = None) -> tuple[str, str, str]:
    provider = VERSION_PROVIDERS[software]

    minor = provider.update_minor(pathlib.Path(path), major, to)

    return provider.NAME, major, minor
