import socket
import threading
import sys
import jwt
from settings import settings

from api.handlers.AuthenticationHandler.AuthHandle import AuthHandle
from api.handlers.ActualUserHandler.UserHandle import UserHandle

class PrivateSocketClient:
    def __init__(self, port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('localhost', port))
        print(f"Connected to private server on port {port}.")
        self.nickname = None

    @staticmethod
    def auth_token(access_token):
        auth_token = AuthHandle(access_token).get_access_token()

        while True:
            try:
                if auth_token['authToken'] == access_token:
                    token_bytes = access_token.encode('utf-8')
                    if not token_bytes:
                        print("Wrong structure of Access Token!!! Please check your token and try again.")
                    else:
                        # Decode the token using the bytes type for the secret key
                        sub = jwt.decode(token_bytes, settings.AUTH_SECRET_KEY.encode('utf-8'), algorithms=['HS256'])
                        dict_string = {'sub': sub, 'message': "Authenticated, login successful!!!"}
                        return dict_string
                else:
                    break
            except Exception as e:
                print("Error: ", e)
                break

    def receive_messages(self):
        while True:
            try:
                data = self.client_socket.recv(1024).decode()
                if data:
                    print(data)
            except Exception as e:
                print("Error receiving message:", e)
                break

    def send_message(self):
        while True:
            try:
                message = f"{self.nickname}: {input('')}"
                self.client_socket.send(message.encode('utf-8'))
            except Exception as e:
                print("Error sending message:", e)
                break

    def start(self):
        access_token = input("Please input the Access Token: ")
        dict_string = PrivateSocketClient.auth_token(access_token=access_token)

        if dict_string['message'] == "Authenticated, login successful!!!":
            user_info = UserHandle(username=dict_string['sub']['sub'].split()[0]).get_user_info()
            self.nickname = user_info['nameaccount']
            print("Authenticated, login successful to name account: {}".format(user_info['nameaccount']))

            self.client_socket.sendall(self.nickname.encode('utf-8'))

            send_thread = threading.Thread(target=self.send_message)
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.start()
            send_thread.start()
        else:
            print("Authentication failed.")

if __name__ == "__main__":
    port = int(sys.argv[1])
    client = PrivateSocketClient(port)
    client.start()