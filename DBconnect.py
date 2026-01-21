import cx_Oracle

class DBconnect:
    def __init__(self, user, passwd, dsn, encoding="UTF-8"):
        self.user = user
        self.passwd = passwd
        self.dsn = dsn
        self.encoding = encoding
        self.connection = None

    def connect(self):
        if self.connection is None:
            self.connection = cx_Oracle.connect(
                user=self.user,
                password=self.passwd,
                dsn=self.dsn,
                encoding=self.encoding
            )
        return self.connection

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None