from api.utils.AuthDbConn import auth_connected


class AuthHandle:
    def __init__(self, accessToken):
        self.accessToken = accessToken

    @staticmethod
    def db_con_auth():
        return auth_connected.connect_collection()

    def getAccessToken(self):  # Remove @staticmethod decorator
        auth_collection = AuthHandle.db_con_auth()
        token = auth_collection.find_one({'authToken': self.accessToken})
        return token
