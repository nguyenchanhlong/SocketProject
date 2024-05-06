from api.utils.DbConn import auth_connected


class AuthHandle:
    def __init__(self, access_token):
        self.accessToken = access_token

    @staticmethod
    def db_con_auth():
        return auth_connected.connect_collection()

    def get_access_token(self):  # Remove @staticmethod decorator
        auth_collection = AuthHandle.db_con_auth()
        token = auth_collection.find_one({'authToken': self.accessToken})
        return token
