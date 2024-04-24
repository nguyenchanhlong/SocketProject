import socket
from settings import settings


def initialize_socket_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_server:
        socket_server.bind((settings.SERVER_HOST, settings.SERVER_PORT))
        socket_server.listen(2)
        """
            connect has the structure {laddr=('127.0.0.1', 65432)}, this is the location of server.
            And address has the structure {laddr=('127.0.0.1', x)}, x mean the random port in our computer to use it for
            the client. "x" can be "41888" or "42562",... 
        """
        connect, address = socket_server.accept()
        print(connect, address)
        print("Connected by", address)
        with connect:
            while True:
                data = connect.recv(1024).decode()
                if not data:
                    break
                print(f"From connected user {address[1]}: " + str(data))
                data = input(" -->")
                connect.sendall(data.encode())


if __name__ == "__main__":
    initialize_socket_server()
