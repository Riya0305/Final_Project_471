# Client Code (client.py)
from socket import *
import os

serverName = "localhost"
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

while True:
    command = input("ftp> ").strip()

    if command.startswith("get"):
        clientSocket.send(command.encode())
        response = clientSocket.recv(1024).decode()
        if response.startswith("EXISTS"):
            file_size = int(response.split()[1])
            user_response = input(f"File exists ({file_size} bytes). Download? (Y/N): ")
            if user_response.lower() == "y":
                clientSocket.send("OK".encode())
                filename = command.split()[1]
                with open(filename, "wb") as f:
                    received_size = 0
                    while received_size < file_size:
                        data = clientSocket.recv(1024)
                        if not data:
                            break
                        f.write(data)
                        received_size += len(data)
                print(f"File {filename} downloaded successfully.")
            else:
                print("Download canceled.")
        else:
            print("File does not exist on server.")

    elif command.startswith("put"):
        filename = command.split()[1]
        if os.path.isfile(filename):
            clientSocket.send(command.encode())
            file_size = os.path.getsize(filename)
            clientSocket.send(str(file_size).encode())
            with open(filename, "rb") as f:
                data = f.read(1024)
                while data:
                    clientSocket.send(data)
                    data = f.read(1024)
            print(f"File {filename} uploaded successfully.")
        else:
            print("File not found.")

    elif command == "ls":
        clientSocket.send(command.encode())
        response = clientSocket.recv(4096).decode()
        print(response)

    elif command == "quit":
        clientSocket.send(command.encode())
        print("Disconnected from server.")
        break

    else:
        print("Invalid command.")

clientSocket.close()