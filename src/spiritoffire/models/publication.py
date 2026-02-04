from pydantic import BaseModel

class Publication(BaseModel):
    target: str
    callback_url: str