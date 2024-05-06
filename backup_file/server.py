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

    def handle_client(self, client_socket, address):
        print(f"Connected to {address}")
        with client_socket:
            self.clients.append((client_socket, address))
            try:
                while True:
                    data = client_socket.recv(1024).decode()
                    if not data:
                        print(f"Connection with {address} closed.")
                        self.clients.remove((client_socket, address))
                        break
                    print(f"Received from {address}: {data}")
                    self.send_to_other_clients(client_socket, data)
            except Exception as e:
                print(f"Error occurred with {address}: {e}")
                self.clients.remove((client_socket, address))

    def send_to_other_clients(self, sender_socket, message):
        for client_socket, client_address in self.clients:
            if client_socket != sender_socket:
                try:
                    # Convert the tuple to a string and then encode
                    client_address_str = f"{message}:{client_address[1]}"
                    client_socket.sendall(client_address_str.encode())
                except Exception as e:
                    print(f"Error sending to {client_address}: {e}")

    def start(self):
        while True:
            client_socket, address = self.server_socket.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, address))
            client_thread.start()


server = SocketServer()
server.start()
