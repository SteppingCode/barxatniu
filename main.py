#imports
import os.path
import sqlite3 as sq
from flask import Flask, redirect, url_for, render_template, g, request
from config import Config
from database.sqldb import DataBase
import git

#variables
app = Flask(__name__)
app.config.from_object(Config)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'base.db'))) #creating database or connecting

def connect_db():
    conn = sq.connect(app.config['DATABASE'])
    conn.row_factory = sq.Row
    return conn

def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
        return g.link_db

"""
#Server updating
@app.route('/update_server', methods=['POST', 'GET'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('/home/ / ')
        origin = repo.remotes.origin
        origin.pull()
        return 'Сайт обновился', 200
    else:
        return 'Возникла ошибка', 400"""


#redirect to start page
@app.route('/')
def start_page():
    db = connect_db()
    database = DataBase(db)
    return render_template('index.html', title='Главная', menu=database.getMenu())

if __name__ == "__main__":
    app.run(debug=True)