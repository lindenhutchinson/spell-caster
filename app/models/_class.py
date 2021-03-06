from app.db.db import db


class _Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    desc = db.Column(db.Text(30000))
    characters = db.relationship("Character", backref='_class', cascade="all, delete", passive_deletes=True)
    spells = db.relationship('SpellClass', backref='_class', cascade="all, delete", passive_deletes=True)


    def __init__(self, name, desc):
        self.name = name
        self.desc = desc

    def __repr__(self):
        return '<Class {}>'.format(self.name) 





