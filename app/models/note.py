from app.db.db import db
import datetime

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    body = db.Column(db.String(5000))
    created_at = db.Column(db.DateTime)

    char_id = db.Column(db.Integer, db.ForeignKey("character.id", ondelete="CASCADE"))

    def __init__(self, title, body, char_id):
        self.title = title
        self.body = body
        self.created_at = datetime.datetime.utcnow()
        self.char_id = char_id
