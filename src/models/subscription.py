from pydantic import BaseModel

class Subscription(BaseModel):
    target: str