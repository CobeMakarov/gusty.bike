class slider_image:
    def __init__(self, db, id, link, order):
        self.db = db

        self.id = id
        self.link = link
        self.pretty_link = link[1:]
        self.order = order

