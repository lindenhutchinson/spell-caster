from app.db.db import db


class Spellbook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    char_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    spell_id = db.Column(db.Integer, db.ForeignKey('spell.id'))
    prepared = db.Column(db.Boolean)


    def __init__(self, character, spell):
        self.character = character
        self.spell = spell
        self.prepared = False


    def __repr__(self):
        return '<Spellbook {}>'.format(self.name) 



