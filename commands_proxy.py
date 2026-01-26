import socket


def proxy(ip, command):
    start_port = 65525
    command = str(command) + "\n"
    for port in range(start_port, start_port + 11):
        server_address = (ip, port)
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        client_socket.settimeout(5)

        try:
            client_socket.connect(server_address)
            client_socket.sendall(command.encode('utf-8'))

            code_cmd = command.split(" ")[0]
            data = client_socket.recv(1024)
            data = data.replace(b"\n", b"")
            data = data.replace(b"\r\n", b"")
            if data.decode('utf-8') == str(code_cmd):
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
