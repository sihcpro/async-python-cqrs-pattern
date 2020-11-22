import json
from uuid import UUID
from datetime import date


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return str(obj)
        if isinstance(obj, date):
            return str(obj)
        return json.JSONEncoder.default(self, obj)
