class UserProperty:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    # Method to convert the object to a dictionary suitable for PyMongo
    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password
        }
