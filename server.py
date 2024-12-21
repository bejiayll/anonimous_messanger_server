import socket
import threading
import time 
import re

class Server: 
    def __init__(self, ip, port):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
        self.server_socket.bind((ip, port))
        self.all_clients = []

        self.server_socket.listen(0)

        print(f"Server is Ready")

        threading.Thread(target=self.connect_handler).start()

    def connect_handler(self):
        while True:
            conn, addr = self.server_socket.accept()
            if conn not in self.all_clients:
                self.all_clients.append(conn)
                threading.Thread(target=self.message_handler, args=(conn, )).start()
    
    def message_handler(self, conn_socket):
        while True:
            message = conn_socket.recv(1024)
            message_content = (str)(message.decode("utf-8"))
            if message_content == "EXIT":
                self.all_clients.remove(conn_socket)
                print(message_content)
                conn_socket.close()
                return
            elif message_content != "":
                self.sendall(conn_socket, bytes(message_content, encoding="utf-8"))
                print(message_content)

            time.sleep(3)

    def sendall(self, conn_socket, message):
        for conn in self.all_clients:
            if conn != conn_socket: 
                conn.send(message)

if __name__ == "__main__":
    server = Server("localhost", 12345)

    