class UserLogin():

    # при создании объекта в декораторе UserLoader
    def fromDB(self, user_id, db):
        self.__user = db.getUser(user_id)
        return self

    def create(self, user):
        self.__user = user
        return self

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.__user['id'])

    def getName(self):
        return self.__user['username'] if self.__user else "Без имени"

    def verifyExt(self, filename):
        ext = filename.rsplit('.', 1)[1]
        if ext == "cpp" or ext == ".h" or ext == ".c" or ext == ".txt" \
                or ext == ".CPP" or ext == ".H" or ext == ".C" or ext == ".TXT":
            return True
        return False
