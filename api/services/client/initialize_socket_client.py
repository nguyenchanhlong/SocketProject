import sys
import os
import threading
import jwt

# Get the absolute path of the directory containing initialize_socket_client.py
current_directory = os.path.dirname(os.path.abspath(__file__))

# Get the parent directory by going up multiple levels
parent_directory = os.path.abspath(os.path.join(current_directory, '../../../'))

# Add the parent directory to the Python path
sys.path.append(parent_directory)

# Now you can import settings
from settings import settings
import socket
from api.handlers.AuthenticationHandler.auth_handle import AuthHandle
from api.handlers.ActualUserHandler.user_handle import UserHandle


class SocketClient:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((settings.SERVER_HOST, settings.SERVER_PORT))
        print("Connected to server.")

        self.username = None
        self.nickname = None
        self.chat_mode = None
        self.target_nickname = None

    @staticmethod
    def auth_token(access_token) -> dict[str, str]:
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
                if data == "NICK":
                    self.client_socket.send(self.nickname.encode('utf-8'))
                else:
                    print(data)
            except Exception as e:
                print("Error receiving message:", e)
                break

    def send_message(self):
        while True:
            try:
                if self.chat_mode == "private":
                    message = f"/private {self.target_nickname} {input('')}"
                else:
                    message = f"{self.nickname}: {input('')}"
                self.client_socket.send(message.encode('utf-8'))
            except Exception as e:
                print("Error sending message:", e)
                break

    def start(self):
        access_token = input("Please input the Access Token: ")
        dict_string = SocketClient.auth_token(access_token=access_token)

        if dict_string['message'] == "Authenticated, login successful!!!":
            user_info = UserHandle(username=dict_string['sub']['sub'].split()[0]).get_user_info()
            self.nickname = user_info['nameaccount']
            print("Authenticated, login successful to name account: {}".format(user_info['nameaccount']))

            self.client_socket.send(self.nickname.encode("utf-8"))
            while True:
                try:
                    mode_prompt = self.client_socket.recv(1024).decode('utf-8')
                    if mode_prompt == "private or group":
                        self.chat_mode = input("Choose chat mode (private/group): ").strip().lower()
                        self.client_socket.send(self.chat_mode.encode('utf-8'))
                        if self.chat_mode == "private":
                            self.target_nickname = input("Enter the nickname of the user you want to chat with: ")
                        break  # Exit the loop after setting the chat mode and nickname
                except Exception as e:
                    print("Error: ", e)
                    break  # Exit the loop in case of an error

            send_thread = threading.Thread(target=self.send_message)
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.start()
            send_thread.start()
        else:
            print("Authentication failed.")


if __name__ == "__main__":
    client = SocketClient()
    client.start()

