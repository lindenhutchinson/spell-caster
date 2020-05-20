from app.db.db import db


class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    race = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    _class = db.relationship("_Class", backref='character', uselist=False)
    slots = db.relationship("Slots", backref='character', uselist=False)
    notes = db.relationship("Notes", backref='character', uselist=False)
    spellbook = db.relationship('Spellbook', backref='character')


    def __init__(self, name, race, user):
        self.name = name
        self.race = race
        self.user = user

    def get_spells(self):
        db.Query.join("")
    def __repr__(self):
        return '<Character {}>'.format(self.name) 





