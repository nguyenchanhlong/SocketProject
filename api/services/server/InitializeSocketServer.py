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

"""
    clients and nicknames have the same of index in the list.
"""


class SocketServer:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((settings.SERVER_HOST, settings.SERVER_PORT))
        self.server_socket.listen(5)
        print("Server is listening for connections...")
        self.clients = []
        self.nicknames = []


    """
        Group chat
    """
    def handle_client(self, client_socket):
        while True:
            try:
                # Send message for all clients Broadcast...
                data = client_socket.recv(1024).decode()
                print(data)
                self.send_to_other_clients(data)
            except Exception as e:
                # the index of client in list of clients
                index = self.clients.index(client_socket)
                self.clients.remove(client_socket)
                client_socket.close()
                nickname = self.nicknames[index]
                self.send_to_other_clients(f'{nickname} left the chat!!!')
                self.nicknames.remove(nickname)
                break

    def send_to_other_clients(self, message):
        for client_socket, client_address in self.clients:
            try:
                client_socket.send(message.encode())
            except Exception as e:
                print("Error: ", e)
                break

    """
        Private chat:
            Client:
                - host: localhost.
                - port: specific port address (12345)
                - nickname: specific nickname.
            Client 1: Port: 55555
            Client 2: Port: 55556
            run main: 
                - private room, group chat:
                    + if choose private room:
                        * input the port you want to connect to communicate.
                - group chat:
    """
    def start(self):
        while True:
            client, address = self.server_socket.accept()
            print(f"Connected by: {str(address)}")

            client.send("NICK".encode('utf-8'))
            nickname = client.recv(1024).decode('utf-8')
            self.nicknames.append(nickname)
            self.clients.append(client, address)
            print('Nickname of the client is {}'.format(nickname))

            client.send("Connected to the server!".encode('utf-8'))
            self.send_to_other_clients(f'{nickname} joined the chat!!!')
            client_thread = threading.Thread(target=self.handle_client, args=(client,))
            client_thread.start()


server = SocketServer()
server.start()
