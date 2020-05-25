import os

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell
from flask_seeder import FlaskSeeder

from app.app import create_app, register_extensions
from app.config.config import DevelopmentConfig
from app.db.db import db

from app.models.user import User
from app.models.character import Character
from app.models._class import _Class
from app.db.seeds.spell_seeder import SpellSeeder, ClassSeeder


app = create_app(DevelopmentConfig)
register_extensions(app)
manager = Manager(app)
migrate = Migrate(app, db)
seeder = ClassSeeder(app)


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
                _Class =_Class
            )

manager.add_command('shell', Shell(make_context=make_shell_context))
# manager.add_command('seed', seeder.run())
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
	manager.run()