import requests


def get_filter_map():
    url = "http://127.0.0.1:5000/perform_query"

    payload = {
        "file_name": "apache_logs.txt",
        "cmd1": "filter",
        "value1": 123,
        "cmd2": "map",
        "value2": "0",
    }

    response = requests.request(method="POST", url=url, data=payload)
    print("===filter_map===")
    print(response.text)
    print("")


def get_unique_map():
    url = "http://127.0.0.1:5000/perform_query"

    payload = {
        'file_name': 'apache_logs.txt',
        'cmd1': 'map',
        'value1': '5',
        'cmd2': 'unique',
        'value2': ''
    }

    response = requests.request("POST", url, data=payload)
    print("===get_unique_map===")
    print(response.text)
    print("")


def get_all_parameters():
    url = "http://127.0.0.1:5000/perform_query"

    payload = {
        "file_name": "apache_logs.txt",
        "cmd1": "filter",
        "value1": "POST",
        "cmd2": "map",
        "value2": "0",
        "cmd342": "unique",
        "value342": "",
        "cmd7": "sort",
        "value7": "asc",
        "cmd6": "limit",
        "value6": "3",
    }

    response = requests.request("POST", url, data=payload)
    print("===get_all_parameters===")
    print(response.text)
    print("")


def get_regex_sort():
    url = "http://127.0.0.1:5000/perform_query"
    payload = {
        "file_name": "apache_logs.txt",
        "cmd1": "regex",
        "value1": "images/\\w+\\.png",
        "cmd2": "sort",
        "value2": "asc",
        "cmd3": "limit",
        "value3": "3"
    }
    response = requests.request("POST", url, data=payload)
    print("===get_regex_sort===")
    print(response.text)


if __name__ == "__main__":
    get_filter_map()
    get_unique_map()
    get_all_parameters()
    get_regex_sort()
