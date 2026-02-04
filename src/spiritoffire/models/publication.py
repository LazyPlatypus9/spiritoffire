from pydantic import BaseModel

from spiritoffire.models import BaseCollection

class Publication(BaseCollection):
    target: str
    callback_url: str