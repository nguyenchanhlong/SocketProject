from typing import Collection
import jwt
from api.models.auth_property import AuthProperty
from api.database_connection import mongo_connection
from settings import settings


def authentication(token_request):
    # Convert the token to bytes before decoding
    token_bytes = token_request.encode('utf-8')
    if not token_bytes:
        return "Unauthorized"
    else:
        # Decode the token using the bytes type for the secret key
        a = jwt.decode(token_bytes, settings.AUTH_SECRET_KEY.encode('utf-8'), algorithms=['HS256'])
        print(a)


if __name__ == "__main__":
    authentication(
        'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJjaGFuaGxvbmdkZXB0cmFpM0BnbWFpbC5jb20gbG9uZ2RlcHRyYWkiLCJleHAiOjE3MTM5NDI4ODd9.SkB7gf3NXPn74UcSo62f-KNNSGzBRq7eO6W-4Bg73d0')
