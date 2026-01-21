from commands import *

class CommandDistribution:
    def __init__(self):
        self.commands = {
            "BC": BCCommand,
            "AC": ACCommand,
            "AD": ADCommand,
            "AW": AWCommand,
            "AB": ABCommand,
            "AR": ARCommand,
            "BA": BACommand,
            "BN": BNCommand,
        }

    def distribute(self, line: bytes, connection, log):
        try:
            code = line[:2]
            code = code.decode("utf-8").upper()
            content = line[2:]
            content = content.decode("utf-8").strip()

            if code in self.commands:
                return self.commands[code](content, connection, log).execute()

            return "ER Unknown command"
        except CommandError as e:
            return str(f"ER {e}")
        except Exception as e:
            return str(f"ER {e}")
