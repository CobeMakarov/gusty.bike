class post:
    def __init__(self, db, id, title, content, creation_date, author, image_path):
        self.db = db

        self.id = id
        self.title = title
        self.content = content
        self.creation_date = creation_date
        self.author = author
        self.image_path = image_path

    def __init__(self, db, id):
        self.db = db

        self.id = id

        self.db.get_cursor().execute("SELECT * FROM posts WHERE id = %s", (self.id,))

        row = self.db.get_cursor().fetchone()

        self.title = row[1]
        self.content = row[2]
        self.creation_date = row[3]
        self.author = row[4]
        self.image_path = row[5]

    @staticmethod
    def create(db, title, content, author, image_path):
        db.get_cursor().execute(
            "INSERT INTO posts (title, content, author_id, image_path) VALUES (%s, %s, %s. %s) RETURNING id",
            (title, content, author, image_path))

        generated = db.get_cursor().fetchone()[0]

        db.commit()

        return generated

    def get_author_name(self):
        self.db.get_cursor().execute("SELECT username FROM users WHERE id = %s", (self.author,))

        row = self.db.get_cursor().fetchone()

        return row[0]

