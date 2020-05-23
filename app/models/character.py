from app.db.db import db


class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    race = db.Column(db.String(128))
    level = db.Column(db.Integer)
    class_resource = db.Column(db.Integer)
    saving_throw = db.Column(db.String(128))
    ability_score = db.Column(db.Integer)
    spell_save = db.Column(db.Integer)
    spell_attack = db.Column(db.Integer)
    prof_bonus = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    class_id = db.Column(db.Integer, db.ForeignKey('class.id', ondelete="CASCADE"))

    slots = db.relationship("Slots", backref='character')
    notes = db.relationship('Note', backref='character', lazy='dynamic', cascade="all, delete", passive_deletes=True)

    spellbook = db.relationship('Spellbook', backref='character')
    

    def __init__(self, name, race, level, saving_throw, ability_score, class_id, user):
        self.name = name
        self.race = race
        self.level = level
        self.class_resource = 2
        self.saving_throw = saving_throw
        self.ability_score =  ability_score
        self.prof_bonus = self.get_prof_bonus()
        self.spell_save = 8 + self.ability_score + self.prof_bonus
        self.spell_attack = self.ability_score + self.prof_bonus
        self.user = user
        self.class_id = class_id

    def get_prof_bonus(self):
        x = self.level/4
        if x <=1:
            return 2
        elif x<=2:
            return 3
        elif x<=3:
            return 4
        elif x<=4:
            return 5
        else:
            return 6

    def __repr__(self):
        return '<Character {}>'.format(self.name) 





