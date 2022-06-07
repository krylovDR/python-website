import sqlite3


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def get_menu(self):
        sql = '''SELECT * FROM mainmenu'''  # выборка всех записей из таблицы
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res:
                return res
        except:
            print("Ошибка чтения их БД")
        return []

    def add_user(self, login, hpsw):
        try:
            self.__cur.execute(f"SELECT COUNT() as `count` FROM users WHERE username LIKE '{login}'")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print("Пользователь с таким логином уже существует")
                return False

            self.__cur.execute("INSERT INTO users VALUES(NULL, ?, ?)", (login, hpsw))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления пользователя в БД " + str(e))
            return False

        return True

    def getUser(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False

            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД " + str(e))

        return False

    def getUserByLogin(self, login):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE username = '{login}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False

            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД " + str(e))

        return False

    def update_password(self, psw, user_id):
        try:
            self.__cur.execute(f"UPDATE users SET psw = ? WHERE id = ?", (psw, user_id))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка при смене пароля в БД: " + str(e))
            return False
        return True

    def update_lab(self, txt, lab, user_id):
        try:
            self.__cur.execute(f"UPDATE users SET {lab} = ? WHERE id = ?", (txt, user_id))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка при смене пароля в БД: " + str(e))
            return False
        return True

