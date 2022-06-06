from flask import Flask, render_template, g, request, abort, flash, session, redirect, url_for
import sqlite3
import os
from FDataBase import FDataBase


# конфигурация
DATABASE = '/tmp/flsite.db'  # путь до файла базы данных
DEBUG = True  # режим отладки
SECRET_KEY = '6d74e6f63a4307f55de5f18b7b64cb2d0ddee5b3'

app = Flask(__name__)
app.config.from_object(__name__)  # загрузка конфигураций

# переопределение пути к базе данных в рабочий каталог
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db')))


# общая функция для установления соединения с базой данных
def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row  # представить в виде словаря, а не картежа
    return conn


# вспомогательная функция для создания таблиц БД
def create_db():
    db = connect_db()  # подключение к бд
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())  # запуск скриптов, содержащихся в sq_db.sql
    db.commit()  # запись изменений в базу данных
    db.close()


# соединение с БД, если оно ещё не установлено
def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


# закрытие соединения с базой данных
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


# декоратор с url-адресом обработчика (/ - главная страница)
@app.route("/")
def index():
    db = get_db()
    dbase = FDataBase(db)
    return render_template('index.html', title="Проверка программ на оформление", menu=dbase.get_menu())


# @app.route("/about")
# def about():
#     return render_template('about.html', title="О сайте", menu=menu)


# @app.route("/contact", methods=["POST", "GET"])
# def contact():
#     if request.method == 'POST':
#         if len(request.form["username"]) >= 2:
#             flash('Сообщение отправлено', category='success')
#         else:
#             flash('Ошибка: Введите username (минимум 2 символа)', category='error')
#
#     return render_template('contact.html', title="Обратная связь", menu=menu)


# @app.route("/profile/<username>")
# def profile(username):
#     if 'userLogged' not in session or session['userLogged'] != username:
#         abort(401)
#
#     return f"Профиль пользователя: {username}"


# @app.route("/login", methods=["POST", "GET"])
# def login():
#     if 'userLogged' in session:
#         return redirect(url_for('profile', username=session['userLogged']))
#     elif request.method == 'POST' and request.form['username'] == "daniil" and request.form["psw"] == "123":
#         session['userLogged'] = request.form['username']
#         return redirect(url_for('profile', username=session['userLogged']))
#
#     return render_template('login.html', title="Авторизация", menu=menu)


@app.errorhandler(404)
def page_not_found(error):
    db = get_db()
    dbase = FDataBase(db)
    return render_template('page404.html', title="Страница не найдена", menu=dbase.get_menu())


# условие для запуска на локальном устройстве
if __name__ == "__main__":
    app.run(debug=True)  # запуск локального веб-сервера, debug, чтобы были ошибки в браузере
