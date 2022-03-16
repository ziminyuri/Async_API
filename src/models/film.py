from typing import Optional

import orjson
from pydantic import BaseModel

from helpers import orjson_dumps


class Film(BaseModel):
    id: str
    title: str
    description: Optional[str]

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
