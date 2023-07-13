import json
from uuid import UUID


class CustomJSONEncoder(json.JSONEncoder):
    """JSON encoder to serialize custom data types."""

    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
        return super().default(obj)
