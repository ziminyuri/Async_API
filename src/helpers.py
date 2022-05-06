from functools import wraps
from hashlib import sha256
from http import HTTPStatus
from pathlib import Path
from time import sleep
from typing import Optional

import orjson
from fastapi import Header, HTTPException

from dictionary import errors_dict


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


def backoff(start_sleep_time=0.1, factor=2,
            border_sleep_time=10, max_attempts=3):
    """
    Функция для повторного выполнения функции через некоторое время, если возникла ошибка.
    Использует наивный экспоненциальный рост времени повтора (factor)
    до граничного времени ожидания (border_sleep_time)

    Формула:
        t = start_sleep_time * 2^(n) if t < border_sleep_time
        t = border_sleep_time if t >= border_sleep_time
    :param start_sleep_time: начальное время повтора
    :param factor: во сколько раз нужно увеличить время ожидания
    :param border_sleep_time: граничное время ожидания
    :param max_attempts: максимальное количество попыток
    :return: результат выполнения функции
    """

    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            time = start_sleep_time
            attempts = max_attempts
            while attempts:
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception:
                    if time >= border_sleep_time:
                        sleep(border_sleep_time)
                    else:
                        sleep(time)
                        time *= factor
                    attempts -= 1
        return inner

    return func_wrapper


def get_key_for_list(index, params):
    key = f'{params}'.encode('utf-8')
    return f'{index}_{str(sha256(key).hexdigest())}'


def get_auth_token(authorization: Optional[str] = Header(None)) -> str:
    if authorization and 'Bearer' in authorization:
        token = authorization.split(' ')[-1]
        return token
    raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=errors_dict['404_token'])


def get_credentials():
    path = Path(__file__).parent
    with open(path.joinpath('grpc_client/certificates/client.key'), 'rb') as f:
        client_key = f.read()
    with open(path.joinpath('grpc_client/certificates/client.pem'), 'rb') as f:
        client_cert = f.read()
    with open(path.joinpath('grpc_client/certificates/ca.pem'), 'rb') as f:
        ca_cert = f.read()

    return client_key, client_cert, ca_cert
