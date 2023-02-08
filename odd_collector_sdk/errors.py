class DataSourceError(Exception):
    pass


class DataSourceAuthorizationError(DataSourceError):
    pass


class DataSourceConnectionError(DataSourceError):
    pass


class MappingDataError(Exception):
    pass


class LoadConfigError(Exception):
    def __init__(self, original_error, *args: object) -> None:
        super().__init__(f"Couldn't handle config. Reason {original_error}", *args)
