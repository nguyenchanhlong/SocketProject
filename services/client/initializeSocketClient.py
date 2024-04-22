import socket
from services.conf.readConf import load_data_server


def initialize_socket_client():
    host, port = load_data_server("../conf/config.json")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_client:
        socket_client.connect((host, port))
        message = input(" --> ")
        while message.lower().strip() != 'quit':
            socket_client.send(message.encode())
            data = socket_client.recv(1024).decode()

            print('Received from server:' + data)

            message = input(" --> ")
        socket_client.close()


if __name__ == "__main__":
    initialize_socket_client()
