import os

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell

from app.app import create_app, register_extensions
from app.config.config import DevelopmentConfig
from app.db.db import db

from app.models.user import User
from app.models.character import Character
from app.models.spell import Spell
from app.models.spellbook import Spellbook
from app.models._class import _Class
from app.models.subclass import Subclass
from app.models.slots import Slots
from app.models.notes import Notes


app = create_app(DevelopmentConfig)
register_extensions(app)
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
	def clear():
		[print() for _ in range(100)]

	def db_add(o):
		db.session.add(o)
		db.session.commit()

	def flush():
		db.session.rollback()

	return dict(app=app,
                db=db, 
                db_add=db_add, 
                flush=flush, 
                clear=clear, 
                User=User, 
                Character=Character, 
                _Class =_Class,
                Subclass=Subclass, 
                Slots=Slots, 
                Spellbook=Spellbook,
                Notes=Notes
            )


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
	manager.run()