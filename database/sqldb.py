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

    def addTeacherMenu(self, title, url):
        try:
            self.__cur.execute("INSERT INTO teachermenu VALUES (NULL, ?, ?)", (title,url))
            self.__db.commit()
        except sq.Error as e:
            print(str(e))
            return False
        return True

    def delTeacherMenu(self, id=0):
        try:
            if id == 0:
                self.__cur.execute("DELETE FROM teachermenu")
            else:
                self.__cur.execute(f"DELETE FROM teachermenu WHERE id == {id}")
            self.__db.commit()
        except sq.Error as e:
            print(str(e))
            return False
        return True

    def getTeacherMenu(self):
        try:
            self.__cur.execute("SELECT * FROM teachermenu")
            res = self.__cur.fetchall()
            if res: return res
        except sq.Error as e:
            print(str(e))
            return False

    def addStudentMenu(self, title, url):
        try:
            self.__cur.execute("INSERT INTO studentmenu VALUES (NULL, ?, ?)", (title,url))
            self.__db.commit()
        except sq.Error as e:
            print(str(e))
            return False
        return True

    def delStudentMenu(self, id=0):
        try:
            if id == 0:
                self.__cur.execute("DELETE FROM studentmenu")
            else:
                self.__cur.execute(f"DELETE FROM studentmenu WHERE id == {id}")
            self.__db.commit()
        except sq.Error as e:
            print(str(e))
            return False
        return True

    def getStudentMenu(self):
        try:
            self.__cur.execute("SELECT * FROM studentmenu")
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

    def getUsers(self, status):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE status = ?", (status,))
            res = self.__cur.fetchall()
            if res: return res
        except sq.Error as e:
            print(str(e))
            return False

    """def getUser(self):
        try:
            self.__cur.execute("SELECT * FROM users WHERE nick = ?", (nick,))
            res = self.__cur.fetchone()
            if res: return res
        except sq.Error as e:
            print(str(e))
            return False"""

    def getStatus(self, nick):
        try:
            self.__cur.execute(f'SELECT * FROM users WHERE nick = ?', (nick,))
            res = self.__cur.fetchone()
            if res: return res[5]
        except sq.Error as e:
            print(str(e))
            return False

    def UpdateStatus(self, nick, status):
        try:
            self.__cur.execute(f"UPDATE users SET status = {status} WHERE nick = {nick}")
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

    def getGames(self):
        try:
            self.__cur.execute(f"SELECT * FROM game")
            res = self.__cur.fetchall()
            if res: return res
        except sq.Error as e:
            print(str(e))
            return False




if __name__ == "__main__":
    db = connect_db()
    db = DataBase(db)
    #create_db()
    #print(db.addMenu('Список игр', 'game_list'))
    #print(db.delUser(0))