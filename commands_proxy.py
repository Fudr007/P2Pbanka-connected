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
            data = data.decode('utf-8').strip()
            data = data.split()
            if str(code_cmd) == 'AB':
                if data[0] == str(code_cmd):
                    return int(data[1])
                elif data[0] == "ER":
                    return f"{data[0]} {data[1]}"
                else:
                    return False
            else:
                print(data)
                if data[0] == str(code_cmd):
                    return True
                elif data[0] == "ER":
                    return f"{data[0]} {data[1]}"
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
