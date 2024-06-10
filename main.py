import threading
import subprocess
import sys
import os

# Get the absolute path of the directory containing InitializeSocketClient.py
current_directory = os.path.dirname(os.path.abspath(__file__))

# Get the parent directory by going up multiple levels
parent_directory = os.path.abspath(os.path.join(current_directory, "../../../"))

# Add the parent directory to the Python path
sys.path.append(parent_directory)


def run_server():
    os.chdir("./api/services/server")
    subprocess.run(["python", "InitializeSocketServer.py"])


def run_api():
    os.chdir("../../../api/routes/ActualUsersRoutes/PersonalInformation")
    subprocess.run(["python", "UsersRoute.py"])


if __name__ == "__main__":
    api_thread = threading.Thread(target=run_api)
    server_thread = threading.Thread(target=run_server)
    server_thread.start()
    # Start the server thread first
    api_thread.start()
    # Then start the API thread
    server_thread.join()
    # Wait for the server thread to finish
    api_thread.join()
    # Wait for the API thread to finish
    print("Server and client have been initialized.")
