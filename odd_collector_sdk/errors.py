class DataSourceError(Exception):
    pass


class DataSourceAuthorizationError(DataSourceError):
    pass


class DataSourceConnectionError(DataSourceError):
    pass


class MappingDataError(Exception):
    pass
