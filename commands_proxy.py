import socket


def proxy(ip, command):
    start_port = 65525
    for port in range(start_port, start_port + 10):
        server_address = (ip, port)

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        client_socket.settimeout(2)

        try:
            client_socket.connect(server_address)

            client_socket.sendall(command.encode('utf-8'))

            data = client_socket.recv(1024)
            if data.decode('utf-8') == "AD":
                return True
            elif data.decode('utf-8').split(" ")[0] == "ER":
                return data.decode('utf-8')
            else:
                return False
        except ConnectionRefusedError:
            continue
        except socket.timeout:
            continue
        except Exception:
            continue

        finally:
            client_socket.close()

    return False