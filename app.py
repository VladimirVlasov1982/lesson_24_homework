import os
from flask import Flask, request
from builder import build_response, check_file_name_key
from exceptions import RequestError

app = Flask(__name__)


@app.route("/perform_query", methods=['POST'])
def perform_query():
    """Получение и обработка запроса"""
    try:
        req = check_file_name_key(dict(request.values.items()))
    except RequestError as error:
        return f"{error.message}", 400
    if not os.path.isfile(f'data/{req.get("file_name")}'):
        return "Файл не найден", 400
    try:
        result = build_response(req)
    except RequestError as error:
        return f"{error.message}", 400
    return app.response_class('\n'.join(result), content_type="text/plain"), 200


if __name__ == "__main__":
    app.run()
