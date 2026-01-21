from datetime import datetime
import multiprocessing
import socket

from DBconnect import DBconnect
from commandDistributor import CommandDistribution

class Server:
    def __init__(self, address, port:int, user, password, dns, encoding, log,timeout:int = 5):
        self._is_running = False
        self.server_inet_address = (address, port)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.timeout = timeout
        self.connection_info = (user, password, dns, encoding)
        self.log = log
        self.run()

    def run(self):
        self._is_running = True
        self.server_socket.bind(self.server_inet_address)
        self.server_socket.listen()
        print(f"Server started at {self.server_inet_address}")
        with open("log.txt", "a") as f:
            f.write(f"{str(datetime.now())} Server started at {self.server_inet_address} \n")

        while self._is_running:
            connection, client_inet_address = self.server_socket.accept()
            multiprocessing.Process(target=ClientHandler, args=(connection, client_inet_address, self.timeout, self.connection_info, self.log)).start()

class ClientHandler:
    def __init__(self, connection, client_inet_address, timeout, connection_info: tuple, log_path):
        self.connection = connection
        self.timeout = timeout
        self.ip = client_inet_address
        self.commandHandling = CommandDistribution()
        self.db_connection = DBconnect(connection_info[0], connection_info[1], connection_info[2], connection_info[3]).connect()
        self.log = log_path
        self.client()

    def client(self):
        self.connection.settimeout(self.timeout)
        with open("log.txt", "a") as f:
            f.write(f"{str(datetime.now())} Client {self.ip} connected \n")
        try:
            with self.connection:
                while True:
                    data = self.connection.recv(256)
                    if not data:
                        break

                    data = data.replace(b"\r\n", b"")
                    response = self.commandHandling.distribute(data, self.db_connection, self.log)
                    self.connection.sendall((response + "\r\n").encode("utf-8"))
                    with open("log.txt", "a") as f:
                        f.write(f"{str(datetime.now())} User {self.ip}, {response} \n")
        except socket.timeout:
            self.db_connection.close()
            self.connection.close()
            print(f"Client {self.ip} timed out")
            with open("log.txt", "a") as f:
                f.write(f"{str(datetime.now())} Client {self.ip} timed out \n")
        except Exception as e:
            print(f"Unexpected error: {e}")
            with open("log.txt", "a") as f:
                f.write(f"{str(datetime.now())} Unexpected error: {e} \n")
        finally:
            self.db_connection.close()
            self.connection.close()
            print(f"Client {self.ip} disconnected")
            with open("log.txt", "a") as f:
                f.write(f"{str(datetime.now())} Client {self.ip} disconnected \n")

    def log(self, operation:str):
        with open("log.txt", "a") as f:
            f.write(f"{operation} from {self.ip}\n")