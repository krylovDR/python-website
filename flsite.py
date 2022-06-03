from flask import Flask, render_template, request


app = Flask(__name__)
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
        print(request.form['username'])

    return render_template('contact.html', title="Обратная связь", menu=menu)


# условие для запуска на локальном устройстве
if __name__ == "__main__":
    app.run(debug=True)  # запуск локального веб-сервера, debug, чтобы были ошибки в браузере
