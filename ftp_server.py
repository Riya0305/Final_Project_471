# FTP Server Code
import socket
import os

def handle_client(conn):
    while True:
        command = conn.recv(1024).decode()
        if not command:
            break
        print(f"Received command: {command}")

        if command.startswith("get"):
            filename = command.split()[1]
            if os.path.isfile(filename):
                conn.send(f"EXISTS {os.path.getsize(filename)}".encode())
                user_response = conn.recv(1024).decode()
                if user_response == "OK":
                    with open(filename, "rb") as f:
                        conn.sendall(f.read())
            else:
                conn.send("ERROR File not found".encode())
        elif command.startswith("put"):
            filename = command.split()[1]
            conn.send("READY".encode())
            with open(filename, "wb") as f:
                data = conn.recv(1024)
                while data:
                    f.write(data)
                    data = conn.recv(1024)
            print(f"File {filename} received")
        elif command == "ls":
            files = os.listdir('.')
            conn.send('\n'.join(files).encode())
        elif command == "quit":
            print("Client disconnected")
            break
        else:
            conn.send("Invalid command".encode())

    conn.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", 2121))
    server_socket.listen(1)
    print("Server is ready to receive")

    while True:
        conn, addr = server_socket.accept()
        print(f"Connection established with {addr}")
        handle_client(conn)

if __name__ == "__main__":
    main()