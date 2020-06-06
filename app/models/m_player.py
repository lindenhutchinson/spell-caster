from app.db.db import db

class MPlayer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    is_active = db.Column(db.Boolean)

    def __init__(self, name):
        self.name = name
        self.is_active = 0

    def __repr__(self):
        return '<Magic Player {}>'.format(self.name)
