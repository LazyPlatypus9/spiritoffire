from pydantic import BaseModel

from spiritoffire.models import BaseCollection

class Consumer(BaseCollection):
    callback_url: str