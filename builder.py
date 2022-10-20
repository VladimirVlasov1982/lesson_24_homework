from dataclasses import dataclass
from typing import Generator, Tuple, List, Optional, Any, Dict
import marshmallow
import marshmallow_dataclass
from marshmallow import ValidationError
import functions
from exceptions import RequestError

CMD_COMMAND: Dict[str, Any] = {
    "filter": functions.filter_query,
    "map": functions.map_query,
    "unique": functions.unique_query,
    "sort": functions.sorted_query,
    "limit": functions.limit_query,
    "regexp": functions.get_regexp,
}


@dataclass
class RequestParam:
    cmd: str
    value: str

    class Meta:
        unknown = marshmallow.EXCLUDE


RequestSchema = marshmallow_dataclass.class_schema(RequestParam)


def check_file_name_key(req: dict) -> dict:
    # Проверяем если аргумент file_name в запросе
    try:
        req["file_name"]
    except KeyError:
        raise RequestError("Аттрибут file_name отсутствует")
    return req


def parse_request(req: dict) -> Tuple[List[RequestParam], Optional[str]]:
    # Обрабатываем запрос, проверяем количество аргументов и их соответствие
    file_name: Optional[str] = req.get("file_name")
    if len(req) % 2 == 0:
        raise RequestError("Неверное количество аргументов в запросе")

    result: List[RequestParam] = []
    lst_cmd: list = [item for item in req.keys() if item.startswith("cmd")]
    lst_value: list = [item for item in req.keys() if item.startswith("value")]
    check_req_param: list = [item for item in req if item not in lst_cmd and item not in lst_value]
    if len(check_req_param) > 1:
        raise RequestError("Неверное название аргументов в запросе")

    if len(lst_cmd) != len(lst_value):
        raise RequestError("Проверьте параметры запроса")

    end_of_cmd: list = list(map(lambda item: item.lstrip("cmd"), lst_cmd))
    end_of_value: list = list(map(lambda item: item.lstrip("value"), lst_value))
    if sorted(end_of_cmd) != sorted(end_of_value):
        raise RequestError("Неверные параметры")

    for i in range(len(lst_cmd)):
        try:
            result.append(RequestSchema().load({"cmd": req[lst_cmd[i]], "value": req[lst_value[i]]}))
        except ValidationError:
            raise RequestError("Неверное значение аргумента. Значение должно быть строкой")

    return result, file_name


def upload_data(file_path: str) -> Generator:
    # Загружаем данне из файла
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            yield line


def build_response(req: dict) -> list:
    # Формируем ответ на запрос
    req_for_command, file_name = parse_request(req)
    result: list = []
    data: Generator | list = upload_data(f"data/{file_name}")
    for item in req_for_command:
        try:
            result = CMD_COMMAND[item.cmd](param=item.value, data=data)
            data = result
        except KeyError:
            raise RequestError(f"{item.cmd} не входит в список команд")
    return result
