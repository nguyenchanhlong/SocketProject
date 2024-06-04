import socket
import threading
import sys

class PrivateSocketServer:
    def __init__(self, port):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('localhost', port))
        self.server_socket.listen(5)
        print(f"Private server is listening on port {port}...")
        self.clients = []
        self.nicknames = {}

    def handle_client(self, client_socket, address):
        print(f"Connected to {address}")
        with client_socket:
            self.clients.append(client_socket)
            try:
                while True:
                    data = client_socket.recv(1024).decode()
                    if not data:
                        print(f"Connection with {address} closed.")
                        self.clients.remove(client_socket)
                        if client_socket in self.nicknames:
                            del self.nicknames[client_socket]
                        break
                    self.broadcast_message(client_socket, data)
            except Exception as e:
                print(f"Error occurred with {address}: {e}")
                self.clients.remove(client_socket)
                if client_socket in self.nicknames:
                    del self.nicknames[client_socket]

    def broadcast_message(self, sender_socket, message):
        sender_nickname = self.nicknames.get(sender_socket)
        for client_socket in self.clients:
            if client_socket != sender_socket:
                try:
                    client_socket.sendall(f"{sender_nickname}: {message}".encode())
                except Exception as e:
                    print(f"Error broadcasting message: {e}")

    def start(self):
        while True:
            client_socket, address = self.server_socket.accept()
            print(f"Connected by: {str(address)}")
            client_socket.send("Please enter your nickname:".encode())
            nickname = client_socket.recv(1024).decode()
            self.nicknames[client_socket] = nickname
            print(f"Nickname of the client is {nickname}")
            client_socket.send("Connected to the server!".encode())
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, address))
            client_thread.start()

if __name__ == "__main__":
    port = int(sys.argv[1])
    server = PrivateSocketServer(port)
    server.start()