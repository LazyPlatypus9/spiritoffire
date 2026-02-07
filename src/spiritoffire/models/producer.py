from spiritoffire.models import BaseCollection

class Producer(BaseCollection):
    source: str
    callback_url: str