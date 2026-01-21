import configparser
import os

import cx_Oracle
from cx_Oracle import connect

from DBconnect import DBconnect


class ConfigError(Exception):
    pass


def load_config(path="config.ini"):
    if not os.path.isfile(path):
        raise ConfigError(f"Config file '{path}' not found.")

    config = configparser.ConfigParser()
    config.read(path)

    if "database" not in config:
        raise ConfigError("Missing [database] section in config file.")

    db = config["database"]

    required = ["user", "password", "host", "port", "service", "encoding"]
    for field in required:
        if field not in db or not db[field].strip():
            raise ConfigError(f"Missing or empty '{field}' in config file.")

    try:
        port = int(db["port"])
        if port <= 0 or port > 65535:
            raise ValueError
    except ValueError:
        raise ConfigError("Port must be a positive integer.")

    dsn = f"{db['host']}:{port}/{db['service']}"

    if "server" not in config:
        raise ConfigError("Missing [server] section in config file.")

    server = config["server"]
    required = ["host", "port", "timeout"]
    for field in required:
        if field not in server or not server[field].strip():
            raise ConfigError(f"Missing or empty '{field}' in config file.")

    try:
        port = int(server["port"])
        if port < 65525 or port > 65535:
            raise ValueError
    except ValueError:
        raise ConfigError("Port must be a positive integer in range 65525-65535.")

    try:
        timeout = int(server["timeout"])
        if timeout <= 0:
            raise ValueError
    except ValueError:
        raise ConfigError("Timeout must be a positive integer.")

    if "path" not in config:
        raise ConfigError("Missing [path] section in config file.")

    path = config["path"]
    required = ["db_code", "log"]
    for field in required:
        if field not in path or not path[field].strip():
            raise ConfigError(f"Missing or empty '{field}' in config file.")

    return {
        "user": db["user"],
        "password": db["password"],
        "dsn": dsn,
        "encoding": db["encoding"],
        "host": server["host"],
        "port": port,
        "timeout": timeout,
        "db_code": path["db_code"],
        "log": path["log"]
    }

def load_sql(user, password, dns, encoding, path="db.sql"):
    try:
        connection = DBconnect(user, password, dns, encoding).connect()
        cursor = connection.cursor()

        with open(path, "r") as f:
            sql_script = f.read()

        for statement in sql_script.split(";"):
            stmt = statement.strip()
            if not stmt:
                continue

            try:
                cursor.execute(stmt)
            except cx_Oracle.DatabaseError as e:
                error_obj, = e.args
                if error_obj.code == 955:
                    continue
                else:
                    raise cx_Oracle.DatabaseError(e)

        connection.commit()
        cursor.close()
        connection.close()
        return True

    except cx_Oracle.DatabaseError as e:
        raise ConfigError(f"database error {e}")
    except Exception as e:
        raise ConfigError(f"{e}")

def create_bank(host_ip, port, user, password, dns, encoding):
    try:
        connection = DBconnect(user, password, dns, encoding).connect()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM bank")
        connection.commit()

        cursor.execute(f"INSERT INTO bank (host_ip, port) VALUES ('{host_ip}', {port})")
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except cx_Oracle.DatabaseError as e:
        return e
    except Exception as e:
        return e