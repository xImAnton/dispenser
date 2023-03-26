from .forge import ForgeVersionProvider
from .paper import PaperVersionProvider
from .vanilla import VanillaVersionProvider, VersionProvider

VERSION_PROVIDERS: dict[str, VersionProvider] = {
    ForgeVersionProvider.NAME: ForgeVersionProvider(),
    PaperVersionProvider.NAME: PaperVersionProvider(),
    VanillaVersionProvider.NAME: VanillaVersionProvider()
}
