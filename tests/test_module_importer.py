import sys
from os import path

from odd_collector_sdk.domain.adapters_initializer import AdaptersInitializer
from odd_collector_sdk.domain.collector_config_loader import CollectorConfigLoader
from tests.plugins.plugins import PLUGIN_FACTORY

test_folder_path = path.realpath(path.dirname(__file__))


def test_importing_modules():
    config_path = path.join(test_folder_path, "collector_config.yaml")
    loader = CollectorConfigLoader(config_path, PLUGIN_FACTORY)
    config = loader.load()

    initializer = AdaptersInitializer("tests.adapters", config.plugins)

    package_name = "tests.adapters.glue"

    assert package_name not in sys.modules
    assert f"{package_name}.adapter" not in sys.modules

    imported_packages = initializer.init_adapters()
    assert f"{package_name}.sub_pkg" in sys.modules
    assert f"{package_name}.sub_pkg.sub_module" in sys.modules

    assert len(imported_packages) == 2
    assert package_name in sys.modules
    assert f"{package_name}.adapter" in sys.modules
