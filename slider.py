from database import database
from slider_image import slider_image


class slider:
    @staticmethod
    def delete(db, id):
        db.get_cursor().execute("DELETE FROM slider_images WHERE id = %s", (id,))

        db.commit()

    def __init__(self, db):

        images = []

        self.db = db

        self.db.get_cursor().execute("SELECT * FROM slider_images ORDER BY slider_order DESC")

        rows = self.db.get_cursor().fetchall()

        for row in rows:
            images.append(slider_image(db, row["id"], row["link"], row["slider_order"]))

        self.images = images

    def upload(self, link, order):
        if order == 0:
            self.db.get_cursor().execute("INSERT INTO slider_images (link, slider_order) VALUES (%s, %s)",
                                         (link, len(self.images)))

            self.db.commit()

            self.refresh()
        else:
            self.db.get_cursor().execute("INSERT INTO slider_images (link, slider_order) VALUES (%s, %s)",
                                         (link, order))

            self.db.commit()

            self.refresh()

    def refresh(self):
        images = []

        self.db.get_cursor().execute("SELECT * FROM slider_images ORDER BY slider_order DESC")

        rows = self.db.get_cursor().fetchall()

        for row in rows:
            images.append(slider_image(self.db, row["id"], row["link"], row["slider_order"]))

        self.images = images
