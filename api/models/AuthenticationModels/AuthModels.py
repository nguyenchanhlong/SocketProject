class AuthProperty:
    def __init__(self, auth_token):
        self.authToken = auth_token

    def to_dict(self):
        return {
            "authToken": self.authToken
        }
