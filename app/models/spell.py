from app.db.db import db

class Spell(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    level = db.Column(db.Integer)
    cast_time = db.Column(db.String(128))
    concentration = db.Column(db.Boolean)
    ritual = db.Column(db.Boolean)
    spell_range = db.Column(db.String(128))
    components = db.Column(db.String(128))
    duration = db.Column(db.String(128))
    school = db.Column(db.String(128))
    info = db.Column(db.String(5000))
    from_book = db.Column(db.String(128))
    is_bard = db.Column(db.Boolean, nullable=True)
    is_cleric = db.Column(db.Boolean, nullable=True)
    is_druid = db.Column(db.Boolean, nullable=True)
    is_paladin = db.Column(db.Boolean, nullable=True)
    is_ranger = db.Column(db.Boolean, nullable=True)
    is_sorcerer = db.Column(db.Boolean, nullable=True)
    is_warlock = db.Column(db.Boolean, nullable=True)
    is_wizard = db.Column(db.Boolean, nullable=True)
    spellbooks = db.relationship("Spellbook", backref='spell')


    def __init__(self, name, level, cast_time, spell_range, components, duration, school, info, from_book, concentration=0,ritual=0, is_bard=0, is_cleric=0, is_druid=0, is_paladin=0, is_ranger=0, is_sorcerer=0, is_warlock=0, is_wizard=0):
        self.name = name
        self.level = level
        self.cast_time=cast_time
        self.concentration=concentration
        self.ritual=ritual
        self.spell_range=spell_range
        self.components = components
        self.duration = duration
        self.school = school
        self.info = info
        self.from_book = from_book
        self.is_bard = is_bard
        self.is_cleric = is_cleric
        self.is_druid = is_druid
        self.is_paladin = is_paladin
        self.is_ranger = is_ranger
        self.is_sorcerer = is_sorcerer
        self.is_warlock = is_warlock
        self.is_wizard = is_wizard

    def __repr__(self):
        return '<Spell {}>'.format(self.name)