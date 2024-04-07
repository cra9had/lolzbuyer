import sqlite3


class TelegramSessionManager:
    DC_INFO = [
        {"ip": '149.154.175.53', "port": 443},
        {"ip": '149.154.167.51', "port": 443},
        {"ip": '149.154.175.100', "port": 443},
        {"ip": '149.154.167.91', "port": 443},
        {"ip": '91.108.56.130', "port": 443}
    ]

    @staticmethod
    def create_telethon_tables(database):
        cursor = database.cursor()
        try:
            cursor.execute("BEGIN TRANSACTION;")
            cursor.execute("CREATE TABLE entities (id integer primary key, hash integer not null, username text, phone integer, name text, date integer)")
            cursor.execute("CREATE TABLE sent_files (md5_digest blob, file_size integer, type integer, id integer, hash integer, primary key(md5_digest, file_size, type))")
            cursor.execute("CREATE TABLE sessions (dc_id integer primary key, server_address text, port integer, auth_key blob, takeout_id integer)")
            cursor.execute("CREATE TABLE update_state (id integer primary key, pts integer, qts integer, date integer, seq integer)")
            cursor.execute("CREATE TABLE version (version integer primary key)")
            database.commit()
        except sqlite3.Error as e:
            print("Error occurred:", e)
            cursor.execute("ROLLBACK;")

    def create_session(self, session_info: dict, file_path="session.session"):
        database = sqlite3.connect(file_path)
        cursor = database.cursor()
        dc_info = self.DC_INFO[session_info["dcId"] - 1]
        self.create_telethon_tables(database)
        cursor.execute("INSERT INTO version (version) VALUES (7);")
        cursor.execute("INSERT INTO sessions (dc_id, server_address, port, auth_key) VALUES (?, ?, ?, ?);", (
            session_info["dcId"], dc_info["ip"], dc_info["port"], bytes.fromhex(session_info["authKey"])))

        database.commit()
        database.close()
        return file_path
