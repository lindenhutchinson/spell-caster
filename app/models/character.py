from app.db.db import db


class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    level = db.Column(db.Integer)
    is_npc = db.Column(db.Boolean)
    # race_id = db.Column(db.Integer, db.ForeignKey('race.id'))
    # condition_id = db.Column(db.Integer, db.ForeignKey('condition.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    class_id = db.Column(db.Integer, db.ForeignKey('class.id', ondelete="CASCADE"))

    actions = db.relationship("Action", backref='character')
    stats = db.relationship("Stats", backref='character')
    slots = db.relationship("Slots", backref='character')
    notes = db.relationship('Note', backref='character', lazy='dynamic', cascade="all, delete", passive_deletes=True)
    spellbook = db.relationship('Spellbook', backref='character')
    

    def __init__(self, name, level, class_id, user,is_npc=0):
        # race_id, condition_id, 
        self.name = name
        self.level = level
        self.is_npc = is_npc
        # self.race_id = race_id
        # self.condition_id = condition_id
        self.class_id = class_id
        self.user = user



    def __repr__(self):
        return '<Character {}>'.format(self.name) 





