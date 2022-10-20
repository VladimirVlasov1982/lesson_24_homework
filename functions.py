import re
from typing import Generator
from exceptions import RequestError


def filter_query(param: str, data: Generator) -> list:
    # Фильтруем данные
    return list(filter(lambda v: param in v, data))


def map_query(param: str, data: Generator) -> list:
    # Выводим данные по номеру столбца
    try:
        column_number = int(param)
    except ValueError:
        raise RequestError("Значение параметра map должно быть числом")
    return list(map(lambda v: v.split(' ')[column_number], data))


def unique_query(data: Generator, *args, **kwargs):
    # Возвращаем уникальные значения
    return list(set(data))


def sorted_query(param: str, data: Generator) -> list:
    # Сортируем данные
    reverse = True if param == 'desc' else False
    return sorted(data, reverse=reverse)


def limit_query(param: str, data: Generator) -> list:
    # Устанавливаем количество строк, которые необходимо вывести
    try:
        limit = int(param)
    except ValueError:
        raise RequestError("Значение параметра limit должно быть целым числом")
    return list(data)[:limit]


def get_regex(param: str, data: Generator) -> list:
    # Находим данные по заданным параметрам
    return list(filter(lambda item: re.search(param, item), data))
