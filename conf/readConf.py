import json
from typing import Any


def load_data_server(filename: str) -> Any:
    with open(filename) as json_file:
        data = json.load(json_file)
    host = data['SocketServer']['HOST']
    port = data['SocketServer']['PORT']
    return host, port
