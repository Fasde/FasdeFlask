from uuid import UUID
from json import JSONEncoder

class UUIDEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return str(obj)
        return JSONEncoder.default(self, obj)
