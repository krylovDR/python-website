from flask import Flask, render_template, request, abort, flash, session, redirect, url_for


app = Flask(__name__)
app.config['SECRET_KEY'] = '9823hiuufsjdbn8iuhlafkef872g3f'

menu = [{"name": "Загрузка кода", "url": "upload-code"},
        {"name": "Личный кабинет", "url": "personal-area"},
        {"name": "Обратная связь", "url": "contact"}]


# декоратор с url-адресом обработчика (/ - главная страница)
@app.route("/")
def index():
    return render_template('index.html', menu=menu)


@app.route("/about")
def about():
    return render_template('about.html', title="О сайте", menu=menu)


@app.route("/contact", methods=["POST", "GET"])
def contact():
    if request.method == 'POST':
        if len(request.form["username"]) >= 2:
            flash('Сообщение отправлено', category='success')
        else:
            flash('Ошибка: Введите username (минимум 2 символа)', category='error')

    return render_template('contact.html', title="Обратная связь", menu=menu)


@app.route("/profile/<username>")
def profile(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)

    return f"Профиль пользователя: {username}"


@app.route("/login", methods=["POST", "GET"])
def login():
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method == 'POST' and request.form['username'] == "daniil" and request.form["psw"] == "123":
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))

    return render_template('login.html', title="Авторизация", menu=menu)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page404.html', title="Страница не найдена", menu=menu)


# условие для запуска на локальном устройстве
if __name__ == "__main__":
    app.run(debug=True)  # запуск локального веб-сервера, debug, чтобы были ошибки в браузере
