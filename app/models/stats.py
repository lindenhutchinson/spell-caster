from app.db.db import db


class Stats(db.Model):
    char_id = db.Column(db.Integer, db.ForeignKey('character.id', ondelete="CASCADE"), primary_key=True)

    str_ = db.Column(db.Integer)
    con_ = db.Column(db.Integer)
    dex_ = db.Column(db.Integer)
    wis_ = db.Column(db.Integer)
    int_ = db.Column(db.Integer)
    chr_ = db.Column(db.Integer)
    ac = db.Column(db.Integer)
    max_hp = db.Column(db.Integer)
    hp = db.Column(db.Integer)
    temp_hp = db.Column(db.Integer, nullable=True)
    spell_save = db.Column(db.Integer,nullable=True)
    spell_attack = db.Column(db.Integer, nullable=True)

    def __init__(self, character, str_, con_, dex_, wis_, int_, chr_, ac, max_hp, spell_save=0, spell_attack=0):
        self.character = character
        self.str_ = str_
        self.con_ = con_
        self.dex_ = dex_
        self.wis_ = wis_
        self.int_ = int_
        self.chr_ = chr_
        self.ac = ac
        self.max_hp = max_hp
        self.hp = max_hp
        self.temp_hp = 0
        self.spell_save = spell_save
        self.spell_attack = spell_attack