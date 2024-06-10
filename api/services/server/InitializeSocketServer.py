import sys
import os
# Get the absolute path of the directory containing InitializeSocketClient.py
current_directory = os.path.dirname(os.path.abspath(__file__))

# Get the parent directory by going up multiple levels
parent_directory = os.path.abspath(os.path.join(current_directory, '../../../'))

# Add the parent directory to the Python path
sys.path.append(parent_directory)
import socket
import threading
from settings import settings


class SocketServer:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((settings.SERVER_HOST, settings.SERVER_PORT))
        self.server_socket.listen(5)
        print("Server is listening for connections...")
        self.clients = []
        self.nicknames = []
        self.private_rooms = {}

    def handle_client(self, client_socket):
        while True:
            try:
                data = client_socket.recv(1024).decode()
                if not data:
                    raise Exception("Disconnected")
                if data.startswith("/private"):
                    _, target_nickname, message = data.split(maxsplit=2)
                    self.send_private_message(client_socket, target_nickname, message)
                else:
                    self.send_to_other_clients(data)
            except Exception:
                index = self.clients.index(client_socket)
                self.clients.remove(client_socket)
                client_socket.close()
                nickname = self.nicknames[index]
                self.send_to_other_clients(f"{nickname} left the chat!!!")
                self.nicknames.remove(nickname)
                break

    def send_to_other_clients(self, message):
        for client_socket in self.clients:
            try:
                client_socket.send(message.encode("utf-8"))
            except Exception as e:
                print("Error: ", e)
                break

    def send_private_message(self, sender_socket, target_nickname, message):
        if target_nickname in self.nicknames:
            target_index = self.nicknames.index(target_nickname)
            target_socket = self.clients[target_index]
            sender_nickname = self.nicknames[self.clients.index(sender_socket)]
            try:
                target_socket.send(f"Private from {sender_nickname}: {message}".encode())
            except Exception as e:
                print("Error: ", e)
        else:
            sender_socket.send(f"User {target_nickname} not found.".encode())

    def start(self):
        while True:
            client, address = self.server_socket.accept()
            print(f"Connected by: {str(address)}")

            client.send("NICK".encode("utf-8"))
            nickname = client.recv(1024).decode("utf-8")
            self.nicknames.append(nickname)
            self.clients.append(client)
            print(f"Nickname of the client is {nickname}")
            client.send("private or group".encode("utf-8"))
            mode = client.recv(1024).decode("utf-8")
            if mode == "private":
                self.server_socket.listen(2)

            else:
                self.server_socket.listen(5)

            self.send_to_other_clients(f"{nickname} joined the chat!!!")
            client.send("Connected to the server!".encode("utf-8"))

            client_thread = threading.Thread(target=self.handle_client, args=(client,))
            client_thread.start()


if __name__ == "__main__":
    server = SocketServer()
    server.start()
