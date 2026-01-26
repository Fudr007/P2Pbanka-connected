from abc import ABC, abstractmethod

from commands_proxy import proxy
from data_layer import DataLayer, DataLayerError


class CommandError(Exception):
    pass

class Command(ABC):
    def __init__(self, command_line: str, connection):
        self.command_line = command_line
        self.data_layer = DataLayer(connection)

    @abstractmethod
    def execute(self) -> str:
        pass

class BCCommand(Command):
    def execute(self) -> str:
        return f"BC {self.data_layer.bank_code()}"

class ACCommand(Command):
    def execute(self) -> str:
        return f"AC {self.data_layer.create_account()}/{self.data_layer.bank_code()}"

class ADCommand(Command):
    def execute(self) -> str:
        try:
            parse_line = self.command_line.split("/")
            acc_number = parse_line[0]
            bank_code = parse_line[1].split(" ")[0]
            deposit_amount = parse_line[1].split(" ")[1]
            if bank_code == self.data_layer.bank_code():
                answer = self.data_layer.deposit(acc_number, deposit_amount)
            else:
                reline = f"AD {acc_number}/{bank_code} {deposit_amount}"
                answer = proxy(bank_code, reline)

            if answer:
                return "AD"
            else:
                raise CommandError(f"ER {answer}")
        except DataLayerError as e:
            raise CommandError(e)
        except Exception as e:
            raise CommandError(f"unexpected {e}")

class AWCommand(Command):
    def execute(self) -> str:
        try:
            parse_line = self.command_line.split("/")
            acc_number = parse_line[0]
            bank_code = parse_line[1].split(" ")[0]
            withdraw_amount = parse_line[1].split(" ")[1]
            if bank_code == self.data_layer.bank_code():
                answer = self.data_layer.withdraw(acc_number, withdraw_amount)
            else:
                reline = f"AW {acc_number}/{bank_code} {withdraw_amount}"
                answer = proxy(bank_code, reline)

            if answer:
                return "AW"
            else:
                raise CommandError(f"ER {answer}")
        except DataLayerError as e:
            raise CommandError(e)
        except Exception as e:
            raise CommandError(f"unexpected {e}")

class ABCommand(Command):
    def execute(self) -> str:
        try:
            parse_line = self.command_line.split("/")
            acc_number = parse_line[0]
            bank_code = parse_line[1]
            if bank_code == self.data_layer.bank_code():
                answer = self.data_layer.balance(acc_number)
            else:
                reline = f"AB {acc_number}/{bank_code}"
                answer = proxy(bank_code, reline)

            if type(answer) == int:
                return f"AB {answer}"
            else:
                raise CommandError(f"ER {answer}")
        except DataLayerError as e:
            raise CommandError(e)
        except Exception as e:
            raise CommandError(f"unexpected {e}")

class ARCommand(Command):
    def execute(self) -> str:
        try:
            parse_line = self.command_line.split("/")
            acc_number = parse_line[0]
            bank_code = parse_line[1]
            if bank_code == self.data_layer.bank_code():
                answer = self.data_layer.delete_account(acc_number)
            else:
                reline = f"AR {acc_number}/{bank_code}"
                answer = proxy(bank_code, reline)

            if answer:
                return "AR"
            else:
                raise CommandError(f"ER {answer}")
        except DataLayerError as e:
            raise CommandError(e)
        except Exception as e:
            raise CommandError(f"unexpected {e}")

class BACommand(Command):
    def execute(self) -> str:
        try:
            return f"BA {self.data_layer.count_money()}"
        except Exception as e:
            raise CommandError(f"unexpected {e}")

class BNCommand(Command):
    def execute(self) -> str:
        try:
            return f"BN {self.data_layer.count_accounts()}"
        except Exception as e:
            raise CommandError(f"unexpected {e}")