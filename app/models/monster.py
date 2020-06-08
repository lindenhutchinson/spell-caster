from app.db.db import db

class Monster(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500))
    url = db.Column(db.String(500))


    def __init__(self, name, url):
        self.name = name
        self.url = url

    def __repr__(self):
        return '<Monster {}>'.format(self.name)

