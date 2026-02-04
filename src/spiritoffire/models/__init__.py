from typing import Optional

from pydantic import BaseModel, Field, ConfigDict

class BaseCollection(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")

    model_config = ConfigDict(populate_by_name=True)