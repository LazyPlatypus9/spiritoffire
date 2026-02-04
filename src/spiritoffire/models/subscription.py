from pydantic import BaseModel

from spiritoffire.models import BaseCollection

class Subscription(BaseCollection):
    target: str