import multiprocessing
import socket

from DBconnect import DBconnect
from commandDistributor import CommandDistribution
from logging import Loging


class Server:
    def __init__(self, address, port:int, user, password, dns, encoding, log,timeout:int = 5):
        self._is_running = False
        self.server_inet_address = (address, port)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.timeout = timeout
        self.connection_info = (user, password, dns, encoding)
        self.logger = Loging(log)
        self.run()

    def run(self):
        self._is_running = True
        self.logger.start()
        self.server_socket.bind(self.server_inet_address)
        self.server_socket.listen()
        self.logger.put_to_queue("info",f"Server started at {self.server_inet_address}")
        try:
            while self._is_running:
                connection, client_inet_address = self.server_socket.accept()
                multiprocessing.Process(target=ClientHandler, args=(connection, client_inet_address, self.timeout, self.connection_info, self.logger)).start()
        except KeyboardInterrupt:
            self.logger.put_to_queue("info", "Server stopped")
        except Exception as e:
            self.logger.put_to_queue("error", f"Unexpected error: {e}")
        finally:
            self._is_running = False
            self.server_socket.close()
            self.logger.stop()

class ClientHandler:
    def __init__(self, connection, client_inet_address, timeout, connection_info: tuple, logger):
        self.connection = connection
        self.timeout = timeout
        self.ip = client_inet_address
        self.commandHandling = CommandDistribution()
        self.db_connection = DBconnect(connection_info[0], connection_info[1], connection_info[2], connection_info[3]).connect()
        self.logger = logger
        self.client()

    def client(self):
        self.connection.settimeout(self.timeout)
        self.logger.put_to_queue("info", f"Client {self.ip} connected")
        try:
            with self.connection:
                while True:
                    data = self.connection.recv(256)
                    if not data:
                        break

                    data = data.replace(b"\r\n", b"")
                    response = self.commandHandling.distribute(data, self.db_connection)
                    self.connection.sendall((response + "\r\n").encode("utf-8"))
                    self.logger.put_to_queue("info", f"User {self.ip}, {response}")
        except socket.timeout:
            self.logger.put_to_queue("info", f"Client {self.ip} timed out")
        except Exception as e:
            self.logger.put_to_queue("error", f"Unexpected error: {e}")
        finally:
            self.db_connection.close()
            self.connection.close()
            self.logger.put_to_queue("info", f"Client {self.ip} disconnected")
