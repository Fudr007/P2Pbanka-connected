from server import Server
from loaders import load_config, load_sql, create_bank

if __name__ == "__main__":
    try:
        config_info = load_config()
        load_sql = load_sql(config_info["user"], config_info["password"], config_info["dsn"], config_info["encoding"], config_info["db_code"])
        create_bank(config_info["host"], config_info["port"], config_info["user"], config_info["password"], config_info["dsn"], config_info["encoding"])
    except Exception as e:
        print(f"ER Config error: {e}")
        exit(1)
    try:
        server = Server(config_info["host"], config_info["port"], config_info["user"], config_info["password"], config_info["dsn"], config_info["encoding"], config_info["log"], timeout = config_info["timeout"])
    except Exception as e:
        print(f"ER Unexpected server error: {e}")