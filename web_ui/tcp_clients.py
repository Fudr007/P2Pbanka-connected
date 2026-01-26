import socket
from dataclasses import dataclass

@dataclass
class TcpConfig:
    host: str = "127.0.0.1"
    port: int = 65530
    timeout_s: int = 2 

class TcpBankClient:
    """
    Jednoduchý TCP klient: pošle text příkaz a přečte odpověď.
    Čtení je "best effort": čte do timeoutu nebo do newline.
    """
    def __init__(self, cfg: TcpConfig | None = None):
        self.cfg = cfg or TcpConfig()

    def set_config(self, host: str, port: int, timeout_s: int = 2):
        self.cfg = TcpConfig(host=host, port=port, timeout_s=timeout_s)

    def send_cmd(self, cmd: str) -> str:
        cmd = cmd.strip()
        if not cmd:
            return "ERROR: empty command"

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(self.cfg.timeout_s)

        try:
            s.connect((self.cfg.host, self.cfg.port))
            s.sendall((cmd + "\n").encode("utf-8"))

            chunks: list[bytes] = []
            while True:
                try:
                    part = s.recv(4096)
                except socket.timeout:
                    break
                if not part:
                    break
                chunks.append(part)
                if b"\n" in part:
                    break

            resp = b"".join(chunks).decode("utf-8", errors="replace").strip()
            return resp if resp else "(no response)"
        finally:
            try:
                s.close()
            except Exception:
                pass
