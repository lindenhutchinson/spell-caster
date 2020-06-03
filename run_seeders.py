import os

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell

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
c_seeder = ClassSeeder(app)
s_seeder = SpellSeeder(app)




# manager.add_command('seed c', c_seeder.run())
manager.add_command('seed s', s_seeder.run())

if __name__ == '__main__':
	manager.run()