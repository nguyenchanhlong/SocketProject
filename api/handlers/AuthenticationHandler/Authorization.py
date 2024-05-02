import jwt
from settings import settings


def authentication(token_request):
    # Convert the token to bytes before decoding
    token_bytes = token_request.encode('utf-8')
    if not token_bytes:
        print("Unauthorized")
    else:
        # Decode the token using the bytes type for the secret key
        a = jwt.decode(token_bytes, settings.AUTH_SECRET_KEY.encode('utf-8'), algorithms=['HS256'])
        print(a)


if __name__ == "__main__":
    authentication('')
