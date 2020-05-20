from app.db.db import db


class _Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    desc = db.Column(db.String(5000))

    # db.relationship("Character", backref="_class")

    def __init__(self, name, desc):
        self.name = name
        self.desc = desc

    def __repr__(self):
        return '<Class {}>'.format(self.name) 





