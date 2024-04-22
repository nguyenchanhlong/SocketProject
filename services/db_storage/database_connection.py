from typing import Any, Mapping

from pymongo import MongoClient
from pymongo.collection import Collection

from services.conf.readConf import load_data_db

host_conf, port_conf, username_conf, password_conf, db_conf, collection_conf = load_data_db("../conf/config.json")


def _connect_db(host: str,
                port: int,
                username: str,
                password: str,
                db: str,
                collection: str) -> MongoClient[Mapping[str, Any] | Any]:
    if username and password:
        mongo_uri = f"mongodb://{username}:{password}@{host}:{port}"
        conn = MongoClient(mongo_uri)
    else:
        conn = MongoClient(host=host, port=port)
    database = conn.get_database(db)
    get_collection = database.get_collection(collection)
    return get_collection


mongo_connection: Collection[Mapping[str, Any] | Any] = _connect_db(
    host=host_conf,
    port=port_conf,
    username=username_conf,
    password=password_conf,
    db=db_conf,
    collection=collection_conf
)
