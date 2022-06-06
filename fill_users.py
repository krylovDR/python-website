import gspread
from werkzeug.security import generate_password_hash
import sqlite3


sa = gspread.service_account(filename="credentials.json")  # используем ключ сервисного аккаунта
sh = sa.open("Vedomost")  # открываем таблицу с ведомостью
wks = sh.worksheet("баллы")  # открываем необходимый лист в таблице ведомости

logins = wks.get('AG5:AG201')  # считывание диапазона ячеек с логинами

# удаление пустых ячеек
for i in range(len(logins) - 1, -1, -1):
    if len(logins[i]) == 0:
        logins.pop(i)

try:
    sqlite_connection = sqlite3.connect('flsite.db')
    cursor = sqlite_connection.cursor()
    print("SQLite connection OK")

    with open('create_users.sql', 'r') as sql_f:
        sql_script = sql_f.read()
    cursor.executescript(sql_script)
    print("SQLite table was created")

    # Добавление админа
    admin = "admin"
    cursor.execute(f"SELECT COUNT() as `count` FROM users WHERE username LIKE '{admin}'")
    res = cursor.fetchone()
    if res[0] > 0:
        print(f"Администратор уже есть")
    else:
        hash = generate_password_hash('1111')  # стандартный пароль для всех в начале
        cursor.execute("INSERT INTO users VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (admin, hash, 1, "", "", "", "", "", "", ""))
        sqlite_connection.commit()
        print(f"Administrator - succefully registered")

    # Добавление студентов
    for i in range(len(logins)):
        cursor.execute(f"SELECT COUNT() as `count` FROM users WHERE username LIKE '{logins[i][0]}'")
        res = cursor.fetchone()
        if res[0] > 0:
            print(f"Пользователь с логином {logins[i][0]} уже существует")
            continue

        hash = generate_password_hash('1111')  # стандартный пароль для всех в начале
        cursor.execute("INSERT INTO users VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (logins[i][0], hash, 0, "", "", "", "", "", "", ""))
        sqlite_connection.commit()
        print(f"Student №{i} - {logins[i][0]} - succefully registered")

    cursor.close()
except sqlite3.Error as error:
    print("Connection failure" + str(error))
finally:
    if (sqlite_connection):
        sqlite_connection.close()
        print("SQLite connection closed")
