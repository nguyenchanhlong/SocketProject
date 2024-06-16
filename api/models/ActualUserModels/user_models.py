class UserProperty:
    def __init__(self, username, password, nameaccount):
        self.username = username
        self.password = password
        self.nameaccount = nameaccount

    # Method to convert the object to a dictionary suitable for PyMongo
    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password,
            "nameaccount": self.nameaccount
        }
