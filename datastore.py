import sqlite3


class DataStore:
    def __init__(self):
        self.connection = sqlite3.connect('students.db')
        self.cursor = self.connection.cursor()
    
    def get_rating(self, username):
        cur = self.connection.cursor()
        result = cur.execute("""SELECT rating FROM students WHERE username = ?""", (username,)).fetchone()
        return str(result[0])

    def add_user(self, user_id, datetime, status):
        with self.connection:
            self.cursor.execute("""INSERT INTO `table_name` (`user_id`, `datetime`, `status`) VALUES (?, ?, ?)""",
                                (user_id, datetime, status))

    def check_user(self, name, surname, patric, cls):
        cur = self.connection.cursor()
        result = cur.execute("""SELECT * FROM students WHERE name = ? AND surname = ? AND patric = ? AND class = ?""", (name, surname, patric, cls)).fetchall()
        return bool(len(result))

    def upd_user_status(self, user_id, status):
        with self.connection:
            return self.cursor.execute("""UPDATE `table_name` SET `status` = ? WHERE `user_id` = ?""", (status, user_id,))

    def get_users(self, status=1):
        with self.connection:
            result = self.cursor.execute("""SELECT `user_id` FROM `table_name` WHERE `status` = ?""", (status,)).fetchall()
            return result

    def close(self):
        self.connection.close()
