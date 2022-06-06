from flask import Flask, render_template, g, request, abort, flash, session, redirect, url_for
import sqlite3
import os
from FDataBase import FDataBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from UserLogin import UserLogin

# конфигурация
DATABASE = '/tmp/flsite.db'  # путь до файла базы данных
DEBUG = True  # режим отладки
SECRET_KEY = '6d74e6f63a4307f55de5f18b7b64cb2d0ddee5b3'
MAX_CONTENT_LENGTH = 1024 * 1024  # максимальный размер файла (1 мбайт)

app = Flask(__name__)
app.config.from_object(__name__)  # загрузка конфигураций

# переопределение пути к базе данных в рабочий каталог
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db')))

login_manager = LoginManager(app)
login_manager.login_view = 'login'  # если не авторизован, будет направлен на login
login_manager.login_message = "Авторизуйтесь, чтобы пользоваться функциями сайта"
login_manager.login_message_category = "success"


@login_manager.user_loader
def load_user(user_id):
    return UserLogin().fromDB(user_id, dbase)


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


# установление соединения с БД перед выполнением запроса
dbase = None
@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = FDataBase(db)


# закрытие соединения с базой данных
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


# декоратор с url-адресом обработчика (/ - главная страница)
@app.route("/")
def index():
    return render_template('index.html', title="Проверка программ на оформление", menu=dbase.get_menu())


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", "success")
    return redirect(url_for('login'))


@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html", menu=dbase.get_menu(), title="Профиль")


@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    if request.method == "POST":
        user = dbase.getUserByLogin(request.form['username'])
        if user and check_password_hash(user['psw'], request.form['psw']):
            userlogin = UserLogin().create(user)
            rm = True if request.form.get('remainme') else False
            login_user(userlogin, remember=rm)
            return redirect(url_for('profile', username=request.form['username']))

        flash("Неверная пара логин/пароль", "error")

    return render_template("login.html", menu=dbase.get_menu(), title="Авторизация")


@app.route("/chpsw", methods=["POST", "GET"])
@login_required
def chpsw():
    if request.method == "POST":
        pswrd1 = request.form['newpsw']
        pswrd2 = request.form['newpsw2']
        if len(pswrd1) > 3 and pswrd1 == pswrd2:
            try:
                hash = generate_password_hash(pswrd1)
                res = dbase.update_password(hash, current_user.get_id())
                if not res:
                    flash("Ошибка смены пароля", "error")
                    return redirect(url_for('chpsw'))
                flash("Пароль изменён", "success")
            except TypeError as e:
                flash("Ошибка при смене пароля", "error")
        else:
            flash("Длина пароля должна быть больше 3, пароль должен совпадать с проверочным", "error")
            return redirect(url_for('chpsw'))
        return redirect(url_for('profile'))
    return render_template("chpsw.html", menu=dbase.get_menu(), title="Смена пароля")


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page404.html', title="Страница не найдена", menu=dbase.get_menu())


@app.route('/upload', methods=["POST", "GET"])
@login_required
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and current_user.verifyExt(file.filename):
            try:
                file_program = file.read()
                print(file_program)
                # ---------------------
            except FileNotFoundError as e:
                flash("Ошибка чтения файла", "error")
        else:
            flash("Ошибка загрузки файла", "error")
    return redirect(url_for('profile'))


# условие для запуска на локальном устройстве
if __name__ == "__main__":
    app.run(debug=True)  # запуск локального веб-сервера, debug, чтобы были ошибки в браузере
