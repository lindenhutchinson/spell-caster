from app.db.db import db


class Subclass(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    desc = db.Column(db.String(5000))
    class_id = db.Column(db.Integer, db.ForeignKey("class.id"))



    def __init__(self, name, desc, _class):
        self.name = name
        self.desc = desc
        self._class = _class

    def __repr__(self):
        return '<Subclass {}>'.format(self.name) 





