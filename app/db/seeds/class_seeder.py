from flask_seeder import Seeder, Faker, generator
from app.models._class import _Class
from app.utils.model_helpers import insert_model
from app.app import create_app, register_extensions
from app.config.config import DevelopmentConfig

# All seeders inherit from Seeder


class ClassSeeder(Seeder):

    # run() will be called by Flask-Seeder
    def run(self):
        self.app = create_app(DevelopmentConfig)
        register_extensions(self.app)

        # Create a new Faker and tell it how to create Class objects
        faker = Faker(
            cls=_Class,
            init={
                "name": generator.Name(),
                "desc": generator.Name()
            }
        )

        # Create 5 class
        with self.app.app_context():
            for _class in faker.create(5):
                print("Adding class: %s" % _class)
                insert_model(_class)
