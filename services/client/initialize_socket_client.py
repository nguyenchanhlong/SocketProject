import socket
from settings import settings


def initialize_socket_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_client:
        socket_client.connect((settings.SERVER_HOST, settings.SERVER_PORT))
        message = input(" --> ")
        while message.lower().strip() != 'quit':
            socket_client.send(message.encode())
            data = socket_client.recv(1024).decode()

            print('Received from server:' + data)

            message = input(" --> ")
        socket_client.close()


if __name__ == "__main__":
    initialize_socket_client()
