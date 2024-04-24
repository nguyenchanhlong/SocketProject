from pymongo.collection import Collection
from api.database_connection import mongo_connection
from settings import settings


class AuthConnection:
    def __init__(self, collection):
        self.collection = collection

    def connect_collection(self):
        database_connection = mongo_connection
        database_connection_auth: Collection = database_connection.get_collection(self.collection)
        return database_connection_auth


auth_connected = AuthConnection(settings.DATABASE_AUTH_COLLECTION)
