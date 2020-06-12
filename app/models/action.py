from app.db.db import db


class Action(db.Model):
    char_id = db.Column(db.Integer, db.ForeignKey('character.id', ondelete="CASCADE"), primary_key=True)
    name = db.Column(db.String(128))
    desc = db.Column(db.String(5000))
    res = db.Column(db.Integer)
    max_res = db.Column(db.Integer)


    def __init__(self, character, name, desc, max_res):
        self.character = character
        self.name = name
        self.desc = desc
        self.max_res = max_res
        self.res = max_res