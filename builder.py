from typing import Generator
import functions
from exceptions import RequestError

VALID_CMD_PARAMS = (
    "filter",
    "map",
    "unique",
    "sort",
    "limit"
)

CMD_VALID_PARAM = {
    "filter": functions.filter_query,
    "map": functions.map_query,
    "unique": functions.unique_query,
    "sort": functions.sorted_query,
    "limit": functions.limit_query,
}


def validate_request(req: dict) -> dict:
    cmd = {}
    value = {}
    try:
        req.get('file_name')
    except KeyError:
        raise RequestError("Аттрибут file_name отсутствует")
    if len(req) % 2 == 0:
        raise RequestError("Неверный запрос, проверьте количество аргументов")
    for key, val in req.items():
        if "cmd" in key.lstrip() and req[key] in VALID_CMD_PARAMS:
            cmd[key] = val
        elif "value" in key.lstrip():
            value[key] = val
    if len(cmd) != len(value):
        raise RequestError("Неверный запрос")
    extra_keys = [item for item in set(req) if item not in set(cmd) and item not in value]
    if len(extra_keys) > 1:
        raise RequestError("Не корректные аргументы")
    return req


def upload_data(file_path: str) -> Generator:
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            yield line


def prepare_request(req: dict) -> list:
    cmd = sorted({key: val for key, val in req.items() if 'cmd' in key.lstrip()})
    value = sorted({key: val for key, val in req.items() if 'value' in key.lstrip()})
    cmd_value = list(zip(cmd, value))
    return cmd_value


def build_query(req: dict) -> list:
    file_name = req.pop('file_name')
    result = []
    cmd_value = prepare_request(req)
    data = upload_data(f"data/{file_name}")
    for item in cmd_value:
        result = CMD_VALID_PARAM[req[item[0]]](param=req[item[1]], data=data)
        data = result
    return result
