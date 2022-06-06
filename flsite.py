from flask import Flask, render_template, request, flash


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


# условие для запуска на локальном устройстве
if __name__ == "__main__":
    app.run(debug=True)  # запуск локального веб-сервера, debug, чтобы были ошибки в браузере
