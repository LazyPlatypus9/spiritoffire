from typing import Optional

from spiritoffire.models import BaseCollection

class Publication(BaseCollection):
    source: str
    callback_url: str

    target: Optional[str | None] = None