import threading
import subprocess
import sys
import os

# Get the absolute path of the directory containing InitializeSocketClient.py
current_directory = os.path.dirname(os.path.abspath(__file__))

# Get the parent directory by going up multiple levels
parent_directory = os.path.abspath(os.path.join(current_directory, '../../../'))

# Add the parent directory to the Python path
sys.path.append(parent_directory)
dir_path = os.path.dirname(__file__)


def run_server():
    os.chdir("./api/services/server")
    subprocess.run(["python", "InitializeSocketServer.py"])


def run_api():
    os.chdir("../../../api/routes/ActualUsersRoutes/PersonalInformation")
    subprocess.run(["python", "UsersRoute.py"])


# # Use threading to run both server and client concurrently
if __name__ == "__main__":
    server_thread = threading.Thread(target=run_server)
    api_thread = threading.Thread(target=run_api)
    # Start the server and client threads
    server_thread.start()
    api_thread.start()

    api_thread.join()
    server_thread.join()

    print("Server and client have been initialized.")
