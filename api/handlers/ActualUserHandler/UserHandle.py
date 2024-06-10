from api.utils.DbConn import user_connected


class UserHandle:
    def __init__(self, username):
        self.username = username

    @staticmethod
    def db_con_user():
        return user_connected.connect_collection()

    def get_user_info(self):
        user_collection = UserHandle.db_con_user()
        user_info = user_collection.find_one({'username': self.username})
        return user_info
