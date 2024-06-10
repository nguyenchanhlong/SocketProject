from typing import Any, Mapping

from pymongo import MongoClient
from pymongo.collection import Collection

from settings import settings


def _connect_db(host: str, port: int, username: str, password: str, db: str) -> Collection:
    if username and password:
        mongo_uri = f"mongodb://{username}:{password}@{host}:{port}"
        conn = MongoClient(mongo_uri)
    else:
        conn = MongoClient(host=host, port=port)
    database = conn.get_database(db)
    return database


mongo_connection: Collection = _connect_db(
    host=settings.DATABASE_HOST,
    port=settings.DATABASE_PORT,
    username=settings.DATABASE_USERNAME,
    password=settings.DATABASE_PASSWORD,
    db=settings.DB,
)
