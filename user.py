from collections import OrderedDict

from werkzeug.security import check_password_hash, generate_password_hash


class user:

    @staticmethod
    def exists(username, db):
        db.get_cursor().execute("SELECT id FROM users WHERE username = %s", (username,))

        count = db.get_cursor().rowcount

        return count == 1

    @staticmethod
    def create(email, password, username, db):

        real_password = generate_password_hash(password)

        db.get_cursor().execute(
            "INSERT INTO users (email, password, username) VALUES (%s, %s, %s) RETURNING id",
            (email, real_password, username))

        generated = db.get_cursor().fetchone()[0]

        db.commit()

        return generated

    @staticmethod
    def login(username, password, db):

        db.get_cursor().execute("SELECT id, password FROM users WHERE username = %s", (username,))

        row = db.get_cursor().fetchone()

        if db.get_cursor().rowcount < 1:
            return False

        id = row[0]
        correct_pw = row[1]

        if check_password_hash(correct_pw, password):
            return id
        else:
            return 0

    def __init__(self, id, db, username=None):
        self.db = db
        self.id = id

        if username is None:
            self.db.get_cursor().execute("SELECT * FROM users WHERE id = %s", (id, ))

            row = self.db.get_cursor().fetchone()

            self.username = row["username"]
            self.rank = row["rank"]
        else:
            self.username = username

