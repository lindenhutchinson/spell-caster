from app.db.db import db


class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    race = db.Column(db.String(128))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    def __init__(self, name, race, user_id):
        self.name = name
        self.race = race
        self.user_id = user_id

    def __repr__(self):
        return '<Character {}>'.format(self.name) 



