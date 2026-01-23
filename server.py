import multiprocessing
import signal
import socket
from threading import Event

from DBconnect import DBconnect
from commandDistributor import CommandDistribution
from logging import Loging


class Server:
    def __init__(self, address, port:int, user, password, dns, encoding, log,timeout:int = 5):
        self.server_inet_address = (address, port)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.timeout = timeout
        self.connection_info = (user, password, dns, encoding)
        self.logger = Loging(log)
        self.clients = []
        self.stop_event = Event()
        signal.signal(signal.SIGINT, self.handle_shutdown)
        signal.signal(signal.SIGTERM, self.handle_shutdown)
        self.run()

    def handle_shutdown(self, sig, frame):
        self.stop_event.set()

    def run(self):
        self.logger.start()
        self.server_socket.settimeout(1.0)
        self.server_socket.bind(self.server_inet_address)
        self.server_socket.listen()
        self.logger.put_to_queue("info",f"Server started at {self.server_inet_address}")
        try:
            while not self.stop_event.is_set():
                try:
                    connection, client_inet_address = self.server_socket.accept()
                    a = multiprocessing.Process(target=ClientHandler, args=(connection, client_inet_address, self.timeout, self.connection_info, self.logger))
                    self.clients.append(a)
                    a.start()

                    self.clients = [c for c in self.clients if c.is_alive()]

                except socket.timeout:
                    continue

        except Exception as e:
            self.logger.put_to_queue("error", f"Unexpected error: {e}")
        finally:
            self.stop()

    def stop(self):
        self.logger.put_to_queue("info", "Server stopped")
        for client in self.clients:
            if client.is_alive():
                client.join(timeout=5)
                client.terminate()

        self.server_socket.close()
        self.logger.stop()
        print("Server stopped safely")

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
