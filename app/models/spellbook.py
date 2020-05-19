from app.db.db import db


class Spellbook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    char_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    spell_id = db.Column(db.Integer, db.ForeignKey('spell.id'))
    prepared = db.Column(db.Boolean)


    def __init__(self, char_id, spell_id):
        self.char_id = char_id
        self.spell_id = spell_id
        self.prepared = False

    def flip_prepare(self):
        self.prepared = not self.prepared

    # def __repr__(self):
    #     return '<Spellbook {}>'.format(self.name) 



