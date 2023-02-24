import traceback
from importlib.metadata import version

from odd_collector_sdk.logger import logger


def print_versions(*pkg_names: str):
    for pkg_name in pkg_names:
        try:
            logger.debug(f"{pkg_name}: {version(pkg_name)}")
        except Exception as e:
            logger.debug(traceback.format_exc())
            logger.warning(f"Could not get version for: {pkg_name}. Reason: {e}")


def print_collector_packages_info(collector_package: str) -> None:
    """Printing collector version with ODD subpackages

    Args:
        collector_package (str): main collector package name
    """
    print_versions(collector_package, "odd_collector_sdk", "odd_models")
