from app.db.db import db


class _Class(db.Model):
    char_id = db.Column(db.Integer, db.ForeignKey('character.id'), primary_key=True)
    name = db.Column(db.String(128))
    level = db.Column(db.Integer)
    desc = db.Column(db.String(5000))
    resource = db.Column(db.Integer)
    saving_throw = db.Column(db.String(128))
    ability_score = db.Column(db.Integer)
    spell_save = db.Column(db.Integer)
    spell_attack = db.Column(db.Integer)
    prof_bonus = db.Column(db.Integer)

    subclass_id = db.Column(db.Integer, db.ForeignKey('subclass.id'))
    subclass = db.relationship("Subclass")

    def __init__(self, char_id, name, level, desc, saving_throw, ability_score, subclass_id):
        self.char_id = char_id
        self.name = name
        self.level = level
        self.desc = desc
        self.resource = 2
        self.saving_throw = saving_throw
        self.ability_score =  ability_score
        self.prof_bonus = self.get_prof_bonus()
        self.spell_save = 8 + self.ability_score + self.prof_bonus
        self.spell_attack = self.ability_score + self.prof_bonus
        self.subclass_id = subclass_id


    def set_resource(self, num):
        self.resource = num

    def change_subclass(self,new_id):
        self.subclass_id = new_id

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
        elif x<=5:
            return 6
        elif x>=6:
            return 6

    




    def __repr__(self):
        return '<Class {}>'.format(self.name) 





