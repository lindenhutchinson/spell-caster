from app.db.db import db


class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    race = db.Column(db.String(128))
    level = db.Column(db.Integer)
    class_resource = db.Column(db.Integer)
    casting_ability = db.Column(db.String(128))
    ability_score = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    class_id = db.Column(db.Integer, db.ForeignKey('class.id', ondelete="CASCADE"))

    slots = db.relationship("Slots", backref='character')
    notes = db.relationship('Note', backref='character', lazy='dynamic', cascade="all, delete", passive_deletes=True)

    spellbook = db.relationship('Spellbook', backref='character')
    

    def __init__(self, name, race, level, casting_ability, ability_score, class_id, user):
        self.name = name
        self.race = race
        self.level = level
        self.class_resource = 2
        self.casting_ability = casting_ability
        self.ability_score =  ability_score
        self.user = user
        self.class_id = class_id


    def __repr__(self):
        return '<Character {}>'.format(self.name) 





