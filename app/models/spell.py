from app.db.db import db

class Spell(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    level = db.Column(db.Integer)
    cast_time = db.Column(db.String(128))
    concentration = db.Column(db.Boolean)
    spell_range = db.Column(db.String(128))
    components = db.Column(db.String(500))
    duration = db.Column(db.String(500))
    school = db.Column(db.String(128))
    info = db.Column(db.String(5000))
    scaling = db.Column(db.String(5000), nullable=True)
    from_book = db.Column(db.String(128), nullable=True)
    is_bard = db.Column(db.Boolean, nullable=True)
    is_cleric = db.Column(db.Boolean, nullable=True)
    is_druid = db.Column(db.Boolean, nullable=True)
    is_paladin = db.Column(db.Boolean, nullable=True)
    is_ranger = db.Column(db.Boolean, nullable=True)
    is_sorcerer = db.Column(db.Boolean, nullable=True)
    is_warlock = db.Column(db.Boolean, nullable=True)
    is_wizard = db.Column(db.Boolean, nullable=True)
    spellbooks = db.relationship("Spellbook", backref='spell')

    
    def __init__(self, name, level, school, cast_time, spell_range, components, duration, text, from_book, scaling=' ', concentration=0,is_bard=0, is_cleric=0, is_druid=0, is_paladin=0, is_ranger=0, is_sorcerer=0, is_warlock=0, is_wizard=0):
    
        self.name = name
        self.level = level
        self.cast_time=cast_time
        self.spell_range=spell_range
        self.components = components
        self.duration = duration
        self.school = school
        self.info = text
        self.from_book = from_book
        self.scaling = scaling
        self.concentration=int(concentration)
        self.is_bard = int(is_bard)
        self.is_cleric = int(is_cleric)
        self.is_druid = int(is_druid)
        self.is_paladin = int(is_paladin)
        self.is_ranger = int(is_ranger)
        self.is_sorcerer = int(is_sorcerer)
        self.is_warlock = int(is_warlock)
        self.is_wizard = int(is_wizard)

    def __repr__(self):
        return '<Spell {}>'.format(self.name)