from database import database
from post import post


class posts:
    def __init__(self, db):

        postz = []

        self.db = db

        self.db.get_cursor().execute("SELECT * FROM posts ORDER BY creation_date DESC")

        rows = self.db.get_cursor().fetchall()

        for row in rows:
            postz.append(post(db, row["id"], row["title"], row["content"], row["creation_date"], row["author_id"], row["image_path"]))

        self.posts = postz

    def refresh(self):
        postz = []

        self.db.get_cursor().execute("SELECT * FROM posts ORDER BY creation_date DESC")

        rows = self.db.get_cursor().fetchall()

        for row in rows:
            postz.append(post(self.db, row["id"], row["title"], row["content"], row["creation_date"], row["author_id"],
                              row["image_path"]))

        self.posts = postz