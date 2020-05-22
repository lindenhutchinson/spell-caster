from app.db.db import db
import datetime
from dateutil import tz

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    body = db.Column(db.String(5000))
    created_at = db.Column(db.DateTime)

    char_id = db.Column(db.Integer, db.ForeignKey("character.id", ondelete="CASCADE"))

    def __init__(self, title, body, char_id):
        self.title = title
        self.body = body
        self.created_at = self.get_local_created_at()
        self.char_id = char_id

    def __repr__(self):
        return '<Note {}>'.format(self.title)

    def get_local_created_at(self):
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
        time = datetime.datetime.utcnow()
        return time.replace(tzinfo=from_zone).astimezone(to_zone)