from app.db.db import db

class Deck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    # strength = db.Column(db.Integer)
    is_com = db.Column(db.Boolean)
    is_active = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime)


    def __init__(self, name, is_com=0):
        self.name = name
        self.is_com = is_com
        self.is_active = 0
        # self.strength = strength

    def __repr__(self):
        return '<Magic Deck {}>'.format(self.name)
