from typing import Optional

import orjson
from pydantic import BaseModel

from helpers import orjson_dumps


class BaseOrjsonModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class InnerFilmModel(BaseOrjsonModel):
    id: str
    title: str
    imdb_rating: Optional[str]
