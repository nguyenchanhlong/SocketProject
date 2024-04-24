from utils.auth_db_conn import auth_connected


class AuthHandle:
    def __init__(self, accessToken):
        self.accessToken = accessToken

    @staticmethod
    def db_con_auth():
        return auth_connected.connect_collection()

    def getAccessToken(self):
        auth_collection = AuthHandle.db_con_auth()
        token = auth_collection.find_one({'accessToken': self.accessToken})
        return token
