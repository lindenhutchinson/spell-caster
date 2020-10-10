from app.db.db import db

class SpellClass(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    spell_id = db.Column(db.Integer, db.ForeignKey('spell.id', ondelete="CASCADE"))
    class_id = db.Column(db.Integer, db.ForeignKey('class.id', ondelete="CASCADE"))


    def __init__(self, _class, spell):
        self._class = _class
        self.spell = spell
        

    def __repr__(self):
        return '<Spellbook {}>'.format(self.id) 
