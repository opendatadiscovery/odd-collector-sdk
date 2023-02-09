from importlib import import_module
from pathlib import Path
from types import ModuleType
from typing import Dict, NamedTuple

from odd_collector_sdk.logger import logger

from .adapter import Adapter
from .plugin import Plugin


class LoadedPackage(NamedTuple):
    package: ModuleType
    adapter: Plugin


def file_match(path: Path) -> bool:
    return path.name.endswith(".py") and not path.name.startswith("__")


def import_submodules(package: ModuleType) -> None:
    package_name = package.__name__
    package_path = Path(package.__file__).parent

    all_files = package_path.glob("*")
    python_modules = filter(file_match, all_files)

    for file in python_modules:
        module_name = f"{package_name}.{file.stem}"
        module = import_module(module_name)

        if file.is_dir():
            import_submodules(module)


class AdaptersInitializer:
    def __init__(self, root_package: str, plugins: list[Plugin]):
        self.root_package = root_package
        self.plugins = plugins

        self.loaded: Dict[str, ModuleType] = {}

    def _load_packages(self) -> list[LoadedPackage]:
        result = []
        for plugin in self.plugins:
            package = self._load_package(plugin)
            loaded = LoadedPackage(package, plugin)
            result.append(loaded)

        return result

    def _load_package(self, plugin: Plugin) -> ModuleType:
        package_path = f"{self.root_package}.{plugin.type}"

        if package_path not in self.loaded:
            package = import_module(package_path)
            import_submodules(package)
            self.loaded[package_path] = package
        else:
            logger.debug(f"Package {package_path=} has been already imported")

        return self.loaded[package_path]

    def init_adapters(
        self,
    ):
        adapters = [
            Adapter(package.adapter.Adapter(plugin), plugin)
            for package, plugin in self._load_packages()
        ]

        logger.success(f"Loaded {len(adapters)} adapter(s).")

        return adapters
