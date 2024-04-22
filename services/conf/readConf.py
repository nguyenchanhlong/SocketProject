import json
from typing import Any


def load_data_server(filename: str) -> Any:
    with open(filename) as json_file:
        data = json.load(json_file)
    host = data['SocketServer']['HOST']
    port = data['SocketServer']['PORT']
    return host, port


def load_data_db(filename: str) -> Any:
    with open(filename) as json_file:
        data = json.load(json_file)
    host_database = data['Database']['DATABASE_HOST']
    port_database = data['Database']['DATABASE_PORT']
    username_database = data['Database']['DATABASE_USERNAME']
    password_database = data['Database']['DATABASE_PASSWORD']
    db = data['Database']['DB']
    collection = data['Database']['DATABASE_COLLECTION']
    return host_database, port_database, username_database, password_database, db, collection
