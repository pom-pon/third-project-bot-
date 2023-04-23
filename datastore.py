import sqlite3


class DataStore:
    def __init__(self):
        self.connection = sqlite3.connect('students.db')
    
    def get_rating(self, username):
        cur = self.connection.cursor()
        result = cur.execute("""SELECT five, four, three, two, concerts, achievements, goverment FROM students WHERE username = ?""", (username,)).fetchone()
        rating = 0.5 * result[0] + 0.2 * result[1] - 0.2 * result[2] - 0.7 * result[3] + 0.3 * result[4] + 0.5 * result[5] + 0.5 * result[6]
        return str(rating)

    def add_user(self, name, surname, patronymic, cls, username, user_id):
        cur = self.connection.cursor()
        id = len(cur.execute("""SELECT * FROM students""").fetchall()) + 1
        five = four = three = two = concerts = achievements = goverment = 0
        studying = False
        cur.execute("""INSERT INTO students (id, studying, name, surname, patronymic, class, username, user_id, five, four, three, two, concerts, achievements, goverment) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (id, studying, name, surname, patronymic, cls, username, user_id, five, four, three, two, concerts, achievements, goverment))
        self.connection.commit()
    
    def verification(self, username):
        cur = self.connection.cursor()
        cur.execute("""UPDATE students SET studying = True WHERE username = ?""", (username,))
        self.connection.commit()

    def check_user(self, name, surname, patronymic, cls):
        name = name[0].upper() + name[1:].lower()
        surname = surname[0].upper() + surname[1:].lower()
        patronymic = patronymic[0].upper() + patronymic[1:].lower()
        cls = cls.replace(' ', '')
        cls = cls[:-1] + cls[-1].upper()
        cur = self.connection.cursor()
        result = cur.execute("""SELECT * FROM students WHERE name = ? AND surname = ? AND patronymic = ? AND class = ?""", (name, surname, patronymic, cls)).fetchall()
        return bool(len(result))
    
    def check_studying(self, username):
        cur = self.connection.cursor()
        result = cur.execute("""SELECT studying FROM students WHERE username = ?""", (username,)).fetchone()
        return bool(result[0])

    def get_email(self, surname, name='', patronymic='', subject=''):
        cur = self.connection.cursor()
        if subject != '':
            result = cur.execute("""SELECT email FROM emails WHERE surname = ? AND subject = ?""", (surname, subject)).fetchall()
        else:
            result = cur.execute("""SELECT email FROM emails WHERE surname = ? AND name = ? AND patronymic = ?""", (surname, name, patronymic)).fetchall()
        return result
    
    def get_users_id(self, cls):
        cur = self.connection.cursor()
        result = cur.execute("""SELECT user_id FROM students WHERE studying = 1 AND class = ?""", (cls,)).fetchall()
        return result


    def close(self):
        self.connection.close()