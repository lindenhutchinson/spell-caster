from app.db.db import db

class Spell(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    # level = db.Column(db.Integer)
    # cast_time = db.Column(db.String(128))
    # spell_range = db.Column(db.String(128))
    # components = db.Column(db.String(128))
    # duration = db.Column(db.String(128))
    # school = db.Column(db.String(128))
    # info = db.Column(db.String(128))
    # from_book = db.Column(db.String(128))
    # is_bard = db.Column(db.Boolean)
    # is_cleric = db.Column(db.Boolean)
    # is_druid = db.Column(db.Boolean)
    # is_paladin = db.Column(db.Boolean)
    # is_ranger = db.Column(db.Boolean)
    # is_sorcerer = db.Column(db.Boolean)
    # is_warlock = db.Column(db.Boolean)
    # is_wizard = db.Column(db.Boolean)

    def __init__(self, name):
        self.name = name
