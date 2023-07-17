"""
In order to serialize custom data types you will need to update this module with appropriate logic.
"""

import json
from uuid import UUID

from flatdict import FlatDict


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
        if isinstance(obj, FlatDict):
            # return str when dict is empty '{}'
            return str(obj.as_dict())
        return super().default(obj)
