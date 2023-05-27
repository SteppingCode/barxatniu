#imports
import os.path
import sqlite3 as sq
from flask import Flask, redirect, url_for, render_template, g, request, session, flash
from config import Config
from database.sqldb import DataBase
import json
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


#Server updating
@app.route('/update_server', methods=['POST', 'GET'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('/home/oduvanchik/barxatniu')
        origin = repo.remotes.origin
        origin.pull()
        return 'Сайт обновился', 200
    else:
        return 'Возникла ошибка', 400


#start page
@app.route('/', methods=['POST', 'GET'])
def start_page():
    db = connect_db()
    database = DataBase(db)
    #login
    if request.method == 'POST':
        if database.getUser(request.form['nick'], request.form['psw']):
            session['userlogged'] = request.form['nick']
        else:
            flash('Неверный логин или пароль', category='error')
    if 'userlogged' in session:
        return render_template('index.html', title='Главная', menu=database.getMenu(), status=database.getStatus(session['userlogged']))
    return render_template('index.html', title='Главная', menu=database.getMenu())

#register
@app.route('/register', methods=['POST', 'GET'])
def register():
    db = connect_db()
    database = DataBase(db)
    if 'userlogged' in session:
        return redirect(url_for('start_page'))
    if request.method == 'POST':
        if request.form['regpsw'] == request.form['regpsw2']:
            if database.addUser(request.form['regnick'], request.form['regpsw'], \
                                    request.form['age'], request.form['regname'], ''):
                session['userlogged'] = request.form['regnick']
                return redirect(url_for('start_page'))
            else:
                flash('Некорректные данные', category='error')
        else:
            flash('Пароли не совпадают', category='error')
    return render_template('register.html', title='Регистрация', menu=database.getMenu())

#admin page
@app.route('/admin', methods=['POST', 'GET'])
def admin_page():
    db = connect_db()
    database = DataBase(db)
    if 'userlogged' in session:
        if database.getStatus(session['userlogged']) == 'admin':
            return render_template('admin.html', menu=database.getMenu(), status=database.getStatus(session['userlogged']))
    return redirect(url_for('start_page'))

#reports
@app.route('/reports', methods=['POST', 'GET'])
def reports_page():
    db = connect_db()
    database = DataBase(db)
    if 'userlogged' in session:
        return render_template('reports.html', menu=database.getMenu(), status=database.getStatus(session['userlogged']))
    return render_template('reports.html', menu=database.getMenu())

#quit
@app.route('/quit')
def quit():
    if 'userlogged' in session:
        return redirect(url_for('start_page')), session.clear()
    else:
        return redirect(url_for('start_page'))

#game list
@app.route('/game_list', methods=['POST', 'GET'])
def game_list():
    db = connect_db()
    database = DataBase(db)
    if 'userlogged' in session:
        return render_template('game_list.html', menu=database.getMenu(), games=database.getGames(),
                               status=database.getStatus(session['userlogged']))
    return render_template('game_list.html', menu=database.getMenu(), games=database.getGames())

if __name__ == "__main__":
    app.run(debug=True)