from typing import Generator

from exceptions import RequestError


def filter_query(param: str, data: Generator) -> list:
    return list(filter(lambda v: param in v, data))


def map_query(param: str, data: Generator) -> list:
    try:
        column_number = int(param)
    except ValueError:
        raise RequestError("Значение параметра map должно быть числом")
    return list(map(lambda v: v.split(' ')[column_number], data))


def unique_query(data: Generator, *args, **kwargs):
    return list(set(data))


def sorted_query(param: str, data: Generator) -> list:
    reverse = True if param == 'desc' else False
    return sorted(data, reverse=reverse)


def limit_query(param: str, data: Generator) -> list:
    try:
        limit = int(param)
    except ValueError:
        raise RequestError("Значение параметра limit должно быть числом")
    return list(data)[:limit]
