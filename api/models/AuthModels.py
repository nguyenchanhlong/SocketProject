class AuthProperty:
    def __init__(self, authToken):
        self.authToken = authToken

    def to_dict(self):
        return {
            "authToken": self.authToken
        }
