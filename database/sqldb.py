import datetime
from datetime import date
import sqlite3 as sq
import os.path
from flask import g, Flask

import os

class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'privet _will day its okey'

app = Flask(__name__)
app.config.from_object(Config)
app.config.update(dict(DATABASE=os.path.join(app.root_path,'../base.db')))



def connect_db():
    conn = sq.connect(app.config['DATABASE'])
    conn.row_factory = sq.Row
    return conn

def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
        return g.link_db

#creating or connecting to database
def create_db():
    '''Вспомогательная функция для создания таблиц БД '''
    db = connect_db()
    with app.open_resource('sql_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()
    return True

class DataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def addMenu(self, title, url):
        try:
            self.__cur.execute("INSERT INTO menu VALUES (NULL, ?, ?)", (title,url))
            self.__db.commit()
        except sq.Error as e:
            print(str(e))
            return False
        return True

    def delMenu(self, id=0):
        try:
            if id == 0:
                self.__cur.execute("DELETE FROM menu")
            else:
                self.__cur.execute(f"DELETE FROM menu WHERE id == {id}")
            self.__db.commit()
        except sq.Error as e:
            print(str(e))
            return False
        return True

    def getMenu(self):
        try:
            self.__cur.execute("SELECT * FROM menu")
            res = self.__cur.fetchall()
            if res: return res
        except sq.Error as e:
            print(str(e))
            return False

    def addUser(self, nick, password, age, name, status):
        try:
            self.__cur.execute("INSERT INTO users VALUES (NULL, ?, ?, ?, ?, ?)", (nick, password, age, name, status))
            self.__db.commit()
        except sq.Error as e:
            print(str(e))
            return False
        return True

    def delUser(self, id=0):
        try:
            if id == 0:
                self.__cur.execute("DELETE FROM users")
            else:
                self.__cur.execute(f"DELETE FROM users WHERE id == {id}")
            self.__db.commit()
        except sq.Error as e:
            print(str(e))
            return False
        return True

    def getUser(self, nick, password):
        try:
            self.__cur.execute(f'SELECT * FROM users WHERE nick == ? AND password == ?', (nick, password))
            res = self.__cur.fetchone()
            if res: return res
        except sq.Error as e:
            print(str(e))
            return False

    def getUsers(self):
        try:
            self.__cur.execute(f"SELECT * FROM users LIMIT 20")
            res = self.__cur.fetchall()
            if res: return res
        except sq.Error as e:
            print(str(e))
            return False

    def getStatus(self, nick):
        try:
            self.__cur.execute(f'SELECT * FROM users WHERE nick = ?', (nick,))
            res = self.__cur.fetchone()
            if res: return res[5]
        except sq.Error as e:
            print(str(e))
            return False

    def UpdateStatus(self, id, status):
        try:
            self.__cur.execute(f"UPDATE users SET status == ? WHERE id == ?", (status, id))
            self.__db.commit()
        except sq.Error as e:
            print(str(e))
            return False
        return True

    def addGame(self, title, info, url):
        try:
            self.__cur.execute("INSERT INTO game VALUES (NULL, ?, ?, ?)", (title, info, url))
            self.__db.commit()
        except sq.Error as e:
            print(str(e))
            return False
        return True

    def delGame(self, id=0):
        try:
            if id == 0:
                self.__cur.execute("DELETE FROM game")
            else:
                self.__cur.execute(f"DELETE FROM game WHERE id == {id}")
            self.__db.commit()
        except sq.Error as e:
            print(str(e))
            return False
        return True

    def getGame(self, arg):
        try:
            self.__cur.execute(f"SELECT * FROM game WHERE id = {arg} LIMIT 1")
            res = self.__cur.fetchone()
            if res: return res
        except sq.Error as e:
            print(str(e))
        return (False, False)

    def getGames(self):
        try:
            self.__cur.execute(f"SELECT * FROM game")
            res = self.__cur.fetchall()
            if res: return res
        except sq.Error as e:
            print(str(e))
            return False

    def addReport(self, user, about, name):
        try:
            tm = date.today()
            self.__cur.execute("INSERT INTO reports VALUES (NULL, ?, ?, ?, ?, ?)", (user, about, tm, name, 'unsolved'))
            self.__db.commit()
        except sq.Error as e:
            print(str(e))
            return False
        return True

    def delReports(self, id=0):
        try:
            if id == 0:
                self.__cur.execute("DELETE FROM reports")
            else:
                self.__cur.execute(f"DELETE FROM reports WHERE id == {id}")
            self.__db.commit()
        except sq.Error as e:
            print(str(e))
            return False
        return True

    def getReports(self):
        try:
            self.__cur.execute(f"SELECT * FROM reports ORDER BY time DESC")
            res = self.__cur.fetchall()
            if res: return res
        except sq.Error as e:
            print(str(e))
        return []

    def getLastReports(self):
        try:
            self.__cur.execute(f"SELECT * FROM reports ORDER BY id DESC LIMIT 5")
            res = self.__cur.fetchall()
            if res: return res
        except sq.Error as e:
            print(str(e))
        return []

    def getReport(self, repid):
        try:
            self.__cur.execute(f"SELECT * FROM reports WHERE id = {repid} LIMIT 1")
            res = self.__cur.fetchone()
            if res: return res
        except sq.Error as e:
            print(str(e))
        return (False, False)

    def getSolvedReports(self):
        try:
            self.__cur.execute(f"SELECT * FROM reports WHERE status == 'solved' ORDER BY time DESC LIMIT 10")
            res = self.__cur.fetchall()
            if res: return res
        except sq.Error as e:
            print(str(e))
        return []

    def getUnSolvedReports(self):
        try:
            self.__cur.execute(f"SELECT * FROM reports WHERE status == 'unsolved' ORDER BY time DESC LIMIT 10")
            res = self.__cur.fetchall()
            if res: return res
        except sq.Error as e:
            print(str(e))
        return []

    def UpdateReportStatus(self, idrep):
        try:
            self.__cur.execute(f"UPDATE reports SET status == 'solved' WHERE id == {idrep}")
            self.__db.commit()
        except sq.Error as e:
            print(str(e))
            return False
        return True

    def addAnswers(self, user, text, idrep):
        try:
            tm = date.today()
            self.__cur.execute("INSERT INTO answers VALUES (NULL, ?, ?, ?, ?)", (user, text, idrep, tm))
            self.__db.commit()
        except sq.Error as e:
            print(str(e))
            return False
        return True

    def delAnswers(self, id=0):
        try:
            if id == 0:
                self.__cur.execute("DELETE FROM answers")
            else:
                self.__cur.execute(f"DELETE FROM answers WHERE id == {id}")
            self.__db.commit()
        except sq.Error as e:
            print(str(e))
            return False
        return True

    def getAnswers(self, id_rep):
        try:
            self.__cur.execute(f"SELECT * FROM answers WHERE idrep == {id_rep} ORDER BY time DESC")
            res = self.__cur.fetchall()
            if res: return res
        except sq.Error as e:
            print(str(e))
        return []

    def addContact(self, user, title, text):
        try:
            time = datetime.date.today()
            self.__cur.execute("INSERT INTO contact VALUES (NULL, ?, ?, ?, ?)", (user, title, text, time))
            self.__db.commit()
        except sq.Error as e:
            print(str(e))
            return False
        return True

    def delContact(self, id=0):
        try:
            if id == 0:
                self.__cur.execute("DELETE FROM contact")
            else:
                self.__cur.execute(f"DELETE FROM contact WHERE id == {id}")
            self.__db.commit()
        except sq.Error as e:
            print(str(e))
            return False
        return True

    def getContacts(self):
        try:
            self.__cur.execute(f"SELECT * FROM contact ORDER BY id DESC LIMIT 20")
            res = self.__cur.fetchall()
            if res: return res
        except sq.Error as e:
            print(str(e))
        return []

    def getContact(self, id):
        try:
            self.__cur.execute(f"SELECT * FROM contact WHERE id == {id}")
            res = self.__cur.fetchone()
            if res: return res
        except sq.Error as e:
            print(str(e))
        return []


if __name__ == "__main__":
    db = connect_db()
    db = DataBase(db)
    #create_db()
    #print(db.addMenu('Список игр', 'game_list'))
    #print(db.delUser(0))
    #print(db.addGame('Quiz', 'Квиз. описание потом напишем', 'quiz'))
    #print(db.addGame('Колесо удачи', 'Колесо удачи. описание потом напишем', 'spin'))
    #print(db.addGame('Найди ошибку', 'Найди ошибку. описание потом напишем', 'find_a_mistake'))