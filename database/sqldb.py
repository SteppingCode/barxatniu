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
            self.__cur.execute(f"SELECT * FROM game WHERE id = {arg}")
            res = self.__cur.fetchone()
            if res:
                return res
        except sq.Error as e:
            print(str(e))
            return (False, False)

    def getGameByUrl(self, url):
        try:
            self.__cur.execute(f"SELECT * FROM game WHERE url == ?", (url,))
            res = self.__cur.fetchone()
            if res: return res
        except sq.Error as e:
            print(str(e))
        return []

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

    def addBook(self, title, description, url, img_url):
        try:
            self.__cur.execute(f"INSERT INTO books VALUES(null, ?, ?, ?, ?)", (title, description, url, img_url))
            self.__db.commit()
        except sq.Error as e:
            print(str(e))
            return False
        return True

    def delBook(self, id=0):
        try:
            if id == 0:
                self.__cur.execute("DELETE FROM books")
            else:
                self.__cur.execute(f"DELETE FROM books WHERE id == {id}")
            self.__db.commit()
        except sq.Error as e:
            print(str(e))
            return False
        return True

    def getBooks(self):
        try:
            self.__cur.execute("SELECT * FROM books")
            res = self.__cur.fetchall()
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
    #print(db.addMenu('Quiz', 'quiz'))
    #print(db.addMenu('Колесо удачи', 'wheel'))
    #print(db.addMenu('Найди ошибку', 'find_a_mistake'))
    #print(db.addMenu('Библиотека', 'books_list'))
    #print(db.addBook('Комфортная книга6', 'Автор: Мэтт Хейг', 'https://www.litres.ru/book/mett-heyg/komfortnaya-kniga-67223155/', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTa02VI6eKCsw3PgZ3XyI_mk9SxSn542ktdXw&usqp=CAU'))
    #print(db.addBook('Книга ведьм6', 'Автор: Кэтрин Хоу', 'https://www.labirint.ru/books/895151/', 'https://img3.labirint.ru/rc/6601f221d65518900b8b805e4ad958ba/363x561q80/books90/895151/cover.jpg?1665480313'))
    #print(db.addBook('Книга ночи6', 'Автор: Холли Блэк', 'https://www.labirint.ru/books/864366/', 'data:image/jpeg;base64,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'))
