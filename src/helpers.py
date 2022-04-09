from functools import wraps
from time import sleep

import orjson


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
