import socket
import os

def send_command(sock, command):
    sock.send(command.encode())
    response = sock.recv(1024).decode()
    print(response)
    return response

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", 2121))
    print("Connected to the server")

    while True:
        command = input("ftp> ").strip()
        if command.startswith("get"):
            filename = command.split()[1]
            response = send_command(client_socket, command)
            if response.startswith("EXISTS"):
                filesize = int(response.split()[1])
                proceed = input(f"File exists ({filesize} bytes). Download? (Y/N) ").strip().upper()
                if proceed == "Y":
                    client_socket.send("OK".encode())
                    with open(filename, "wb") as f:
                        data = client_socket.recv(1024)
                        total_received = len(data)
                        while data:
                            f.write(data)
                            if total_received >= filesize:
                                break
                            data = client_socket.recv(1024)
                            total_received += len(data)
                    print(f"File {filename} downloaded successfully.")
                else:
                    client_socket.send("CANCEL".encode())
            else:
                print("File not found on server.")
        elif command.startswith("put"):
            filename = command.split()[1]
            if os.path.isfile(filename):
                send_command(client_socket, command)
                with open(filename, "rb") as f:
                    client_socket.sendall(f.read())
                print(f"File {filename} uploaded successfully.")
            else:
                print("File not found locally.")
        elif command in ["ls", "quit"]:
            send_command(client_socket, command)
            if command == "quit":
                break
        else:
            print("Invalid command.")

    client_socket.close()

if __name__ == "__main__":
    main()