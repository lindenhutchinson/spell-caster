import os

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell

from app.app import create_app, register_extensions
from app.config.config import DevelopmentConfig
from app.db.db import db

from app.db.seeds.spell_seeder import SpellSeeder
from app.db.seeds.class_seeder import ClassSeeder


app = create_app(DevelopmentConfig)
register_extensions(app)
manager = Manager(app)
migrate = Migrate(app, db)
c_seeder = ClassSeeder(app)
s_seeder = SpellSeeder(app)

@manager.command
def _class():
	c_seeder.run()

@manager.command
def spell():
	s_seeder.run()

if __name__ == '__main__':
	manager.run()