from app.db.db import db


class Spellbook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    char_id = db.Column(db.Integer, db.ForeignKey('character.id', ondelete="CASCADE"))
    spell_id = db.Column(db.Integer, db.ForeignKey('spell.id', ondelete="CASCADE"))
    prepared = db.Column(db.Boolean)


    def __init__(self, char_id, spell):
        self.char_id = char_id
        self.spell = spell
        self.prepared = False


    def __repr__(self):
        return '<Spellbook {}>'.format(self.id) 



