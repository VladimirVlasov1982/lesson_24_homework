import os
from flask import Flask, request
from builder import build_query, validate_request
from exceptions import RequestError

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


@app.route("/perform_query", methods=['POST'])
def perform_query():
    try:
        req = validate_request(dict(request.values.items()))
    except RequestError as error:
        return f"{error.message}", 400
    if not os.path.isfile(f'data/{req["file_name"]}'):
        return "Файл не найден", 400
    try:
        result = build_query(req)
    except RequestError as error:
        return f"{error.message}", 400
    return app.response_class('\n'.join(result), content_type="text/plain"), 200


if __name__ == "__main__":
    app.run()
