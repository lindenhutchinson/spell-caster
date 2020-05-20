from app.db.db import db
from app.models.character import Character
from app.models._class import _Class


class Slots(db.Model):
    slot_id = db.Column(db.String(128), primary_key=True)
    char_id = db.Column(db.Integer, db.ForeignKey('character.id'))

    lvl = db.Column(db.Integer)
    max_val = db.Column(db.Integer)
    cur_val = db.Column(db.Integer)


    def __init__(self, lvl, max_val, character):
        self.character = character
        self.slot_id = "{}-{}".format(character.id, lvl)
        self.lvl = lvl
        self.max_val = max_val
        self.cur_val = max_val

    # def get_char(self):
    #     return db.session.query(_Class).filter(Character.id == self.char_id).join(_Class).filter(Character.id == _Class.char_id).one_or_none()

   