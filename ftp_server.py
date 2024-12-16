# Server Code (serv.py)
from socket import *
import os

# Server setup
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("", serverPort))
serverSocket.listen(1)
print("The server is ready to receive")

while True:
    connectionSocket, addr = serverSocket.accept()
    while True:  # Keep the connection open for multiple commands
        command = connectionSocket.recv(1024).decode()

        if not command:  # Break the loop if no command is received (client disconnected)
            break

        if command.startswith("get"):
            filename = command.split()[1]
            if os.path.isfile(filename):
                file_size = os.path.getsize(filename)
                connectionSocket.send(f"EXISTS {file_size}".encode())
                user_response = connectionSocket.recv(1024).decode()
                if user_response == "OK":
                    with open(filename, "rb") as f:
                        data = f.read(1024)
                        while data:
                            connectionSocket.send(data)
                            data = f.read(1024)
                print(f"File {filename} sent successfully.")
            else:
                connectionSocket.send("ERR".encode())

        elif command.startswith("put"):
            filename = command.split()[1]
            file_size = int(connectionSocket.recv(1024).decode())
            with open(filename, "wb") as f:
                received_size = 0
                while received_size < file_size:
                    data = connectionSocket.recv(1024)
                    if not data:
                        break
                    f.write(data)
                    received_size += len(data)
            print(f"File {filename} received successfully.")

        elif command == "ls":
            files = "\n".join(os.listdir())
            connectionSocket.send(files.encode())

        elif command == "quit":
            print("Client disconnected.")
            connectionSocket.close()
            break  # Close connection after quit command

        else:
            connectionSocket.send("Invalid command".encode())

    connectionSocket.close()