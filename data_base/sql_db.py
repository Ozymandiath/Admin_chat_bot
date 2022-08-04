import sqlite3 as sq
import time


class Database():
    def __init__(self, db_file):
        self.db = sq.connect(db_file)
        self.cursor = self.db.cursor()
        if self.db:
            print("Date base connected OK")
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY, 
            user_id INTEGER, 
            nickname VARCHAR(100), 
            job_title VARCHAR DEFAULT 'user', 
            subscription BOOLEAN NOT NULL DEFAULT 0)
        """)

    def add_user(self, user_id, user_nickname):
        with self.db:
            self.cursor.execute("INSERT INTO users(user_id, nickname) VALUES(?,?)", (user_id, user_nickname))

    def user_presence(self, user_id):
        with self.db:
            result = self.cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,)).fetchone()
            return result is None

    def user_list(self):
        result = []
        with self.db:
            list = self.cursor.execute("SELECT user_id FROM users").fetchall()
            for i in list:
                result.append(i[0])
            return result

    def admin_check(self, user_id):
        with self.db:
            result = self.cursor.execute("SELECT job_title FROM users WHERE user_id = ?",
                                         (user_id,)).fetchone()[0]
            return result == "admin"

    def set_time_sub(self, user_id, time_sub):
        with self.db:
            self.cursor.execute("UPDATE users SET subscription = ? WHERE user_id = ?", (time_sub, user_id))

    def get_time_sub(self, user_id):
        with self.db:
            user_time = self.cursor.execute("SELECT subscription FROM users WHERE user_id = ?",
                                            (user_id,)).fetchone()[0]
            return int(user_time)

    def get_status_sub(self, user_id):
        with self.db:
            user_time = self.cursor.execute("SELECT subscription FROM users WHERE user_id = ?",
                                            (user_id,)).fetchone()[0]
            return True if int(user_time) > int(time.time()) else False
