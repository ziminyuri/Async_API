import hashlib

import orjson


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


def get_hash(*args) -> str:
    parts = "".join([str(arg) for arg in args]).encode('UTF-8')
    hash_ = hashlib.sha256(parts)
    return str(hash_.hexdigest())
