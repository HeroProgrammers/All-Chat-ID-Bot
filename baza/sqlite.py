import sqlite3
import time

class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        connection = sqlite3.connect(self.path_to_db)
        connection.execute("PRAGMA journal_mode=WAL;")  # WAL journal mode for concurrency
        connection.isolation_level = None  # Autocommit mode
        return connection

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users(
        full_name TEXT,
        telegram_id NUMBER unique,
        language TEXT 
        );
        """
        self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([f"{item} = ?" for item in parameters])
        return sql, tuple(parameters.values())

    def add_user(self, telegram_id: int, full_name: str, language: str):
        sql = """
        INSERT INTO Users(telegram_id, full_name, language) VALUES(?, ?, ?);
        """
        self.execute(sql, parameters=(telegram_id, full_name, language), commit=True)

    def select_all_users(self):
        sql = "SELECT * FROM Users;"
        return self.execute(sql, fetchall=True)

    def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE 1=1;"
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)

    def delete_users(self):
        self.execute("DELETE FROM Users WHERE TRUE;", commit=True)

    def all_users_id(self):
        nat = self.execute("SELECT telegram_id FROM Users;", fetchall=True)
        return [user_id[0] for user_id in nat]

    def get_lang(self, user_id):
        sql = "SELECT language FROM Users WHERE telegram_id = ?;"
        result = self.execute(sql, parameters=(user_id,), fetchone=True)
        return result[0] if result else None

    def update_lang(self, user_id, language):
        try:
            connection = self.connection
            cursor = connection.cursor()
            cursor.execute("BEGIN TRANSACTION;")
            cursor.execute("UPDATE Users SET language=? WHERE telegram_id=?", (language, user_id))
            cursor.execute("COMMIT;")
        except sqlite3.OperationalError as e:
            print(f"Error: {e}")
            if "database is locked" in str(e):
                time.sleep(1) 
                self.update_lang(user_id, language)  
        finally:
            connection.close()

def logger(statement):
    print(f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
""")

