from database import database
from post import post


class posts:
    def __init__(self, db):

        postz = []

        self.db = db

        self.db.get_cursor().execute("SELECT * FROM posts ORDER BY created DESC")

        rows = self.db.get_cursor().fetchall()

        for row in rows:
            postz.append(post(db, row["id"], row["title"], row["content"], row["created"], row["author_id"],
                              row["image_path"]))

        self.posts = postz

    def most_recent(self, omit=0):
        safe_posts = [p for p in self.posts if p.id != omit]

        return safe_posts[:3]

    def refresh(self):
        postz = []

        self.db.get_cursor().execute("SELECT * FROM posts ORDER BY created DESC")

        rows = self.db.get_cursor().fetchall()

        for row in rows:
            postz.append(post(self.db, row["id"], row["title"], row["content"], row["created"], row["author_id"],
                              row["image_path"]))

        self.posts = postz
