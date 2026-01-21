import cx_Oracle

class DataLayerError(Exception):
    pass

class DataLayer:
    def __init__(self, connection):
        self.connection = connection

    def bank_code(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT host_ip FROM bank")
            code = str(cursor.fetchone()[0])
            cursor.close()
            return code
        except Exception as e:
            raise DataLayerError(e)

    def create_account(self):
        try:
            cursor = self.connection.cursor()
            acc_number = cursor.var(cx_Oracle.NUMBER)
            cursor.execute("INSERT INTO bank_account (balance) VALUES (DEFAULT) RETURNING acc_number INTO :acc_number", acc_number=acc_number)
            self.connection.commit()
            acc_number = int(acc_number.getvalue()[0])
            cursor.close()
            return acc_number
        except Exception as e:
            raise DataLayerError(e)

    def deposit(self, acc_number, deposit_amount, ):
        try:
            acc_number = int(acc_number)
            deposit_amount = int(deposit_amount)
            if deposit_amount <= 0:
                raise ValueError("Deposit amount must be positive")
            if acc_number < 10000 or acc_number > 99999:
                raise ValueError("Invalid account number")

            cursor = self.connection.cursor()
            cursor.execute(f"SELECT * FROM bank_account WHERE acc_number = {acc_number}")
            if not cursor.fetchone():
                raise DataLayerError("Account not found")
            cursor.execute(f"UPDATE bank_account SET balance = balance + {deposit_amount} WHERE acc_number = {acc_number}")
            self.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            raise DataLayerError(e)

    def withdraw(self, acc_number, withdraw_amount):
        try:
            acc_number = int(acc_number)
            withdraw_amount = int(withdraw_amount)
            if withdraw_amount <= 0:
                raise ValueError("Withdraw amount must be positive")
            if acc_number < 10000 or acc_number > 99999:
                raise ValueError("Invalid account number")

            cursor = self.connection.cursor()
            cursor.execute(f"SELECT balance FROM bank_account WHERE acc_number = {acc_number}")
            balance = cursor.fetchone()[0]
            if not balance:
                raise DataLayerError("Account not found")
            if int(balance) < withdraw_amount:
                raise DataLayerError("Insufficient funds")
            cursor.execute(f"UPDATE bank_account SET balance = balance - {withdraw_amount} WHERE acc_number = {acc_number}")
            self.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            raise DataLayerError(e)

    def balance(self, acc_number):
        try:
            acc_number = int(acc_number)
            if acc_number < 10000 or acc_number > 99999:
                raise ValueError("Invalid account number")

            cursor = self.connection.cursor()
            cursor.execute(f"SELECT * FROM bank_account WHERE acc_number = {acc_number}")
            if not cursor.fetchone():
                raise DataLayerError("Account not found")
            cursor.execute(f"SELECT balance FROM bank_account WHERE acc_number = {acc_number}")
            balance = int(cursor.fetchone()[0])
            cursor.close()
            return balance
        except Exception as e:
            raise DataLayerError(e)

    def delete_account(self, acc_number):
        try:
            acc_number = int(acc_number)
            if acc_number < 10000 or acc_number > 99999:
                raise ValueError("Invalid account number")

            cursor = self.connection.cursor()
            cursor.execute(f"SELECT * FROM bank_account WHERE acc_number = {acc_number}")
            if not cursor.fetchone():
                raise DataLayerError("Account not found")
            cursor.execute(f"DELETE FROM bank_account WHERE acc_number = {acc_number}")
            self.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            raise DataLayerError(e)

    def count_money(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT SUM(balance) FROM bank_account")
            res = cursor.fetchone()
            if not res:
                money = 0
            else:
                money = int(res[0])
            cursor.close()
            return money
        except Exception as e:
            raise DataLayerError(e)

    def count_accounts(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM bank_account")
            res = cursor.fetchone()
            if not res:
                acc_count = 0
            else:
                acc_count = int(res[0])
            cursor.close()
            return acc_count
        except Exception as e:
            raise DataLayerError(e)