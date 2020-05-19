from app.db.db import db


class Subclass(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    desc = db.Column(db.String(5000))
    resource_name = db.Column(db.String(128))



    def __init__(self, name, desc, resource_name):
        self.name = name
        self.desc = desc
        self.resource_name = resource_name

    def __repr__(self):
        return '<Subclass {}>'.format(self.name) 





